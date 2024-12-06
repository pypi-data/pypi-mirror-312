import re
import http.client
import base64
import json
import logging
from urllib.parse import urlparse
from typing import Optional, Union

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class PageManager:
    def __init__(
        self, page_id: str, server_url: str, auth_username: str, auth_token: str
    ):
        """
        Initialize the PageManager with connection details.

        Parameters:
        - page_id (str): The ID of the Confluence page to interact with.
        - server_url (str): The base URL of the Confluence server (e.g., "https://demo.atlassian.com").
        - auth_username (str): The username for Basic Authentication.
        - auth_token (str): The token for Basic Authentication.
        """
        self.page_id = page_id

        self._server_url = server_url
        self._server_port = 443 if server_url.startswith("https") else 80
        self._auth_username = auth_username
        self._auth_token = auth_token
        self._http_connection = None
        self._auth_headers = self._create_authentication_headers()
        

        self._html_header = None
        self._html_title = None
        self._html_table_key = "Key"
        self._html_table_value = "Value"

        self.open()

    def set_html_header(self, header: str, paragraph: str, title: str = None, table_key: str = None, table_value: str = None):
        """
        Set the HTML header for the page.

        Parameters:
        - header (str): The header text.
        - paragraph (str): The paragraph text.
        """
        self._html_header = f"<h1>{header}</h1><p>{paragraph}</p>"
        self._html_title = title

        if table_key:
            self._html_table_key = table_key

        if table_value:
            self._html_table_value = table_value
        
    def _create_authentication_headers(self) -> dict:
        """
        Create the Authorization headers for Basic Authentication.

        Returns:
        - dict: A dictionary containing the Authorization header with a Basic authentication token.

        Raises:
        - ValueError: If there's an error in creating the authentication headers.
        """
        try:
            auth_string = f"{self._auth_username}:{self._auth_token}"
            auth_bytes = base64.b64encode(auth_string.encode("utf-8"))
            logger.debug("Authorization headers created successfully.")
            return {"Authorization": f"Basic {auth_bytes.decode('utf-8')}"}
        except Exception as e:
            logger.error(f"Failed to create auth headers, error: {e}")
            raise ValueError("Error creating authentication headers.") from e

    def open(self):
        """
        Establish a connection to the Confluence server.

        Raises:
        - ConnectionError: If the connection to the server fails.
        """
        try:
            parsed_url = urlparse(self._server_url)
            if parsed_url.scheme == "https":
                self._http_connection = http.client.HTTPSConnection(
                    parsed_url.netloc, self._server_port, timeout=10
                )
            else:
                self._http_connection = http.client.HTTPConnection(
                    parsed_url.netloc, self._server_port, timeout=10
                )

            logger.debug(f"Connected to Confluence server at {self._server_url}.")
        except (http.client.HTTPException, OSError) as e:
            logger.error(f"Failed to connect to Confluence server: {e}")
            raise ConnectionError(f"Unable to connect to {self._server_url}.") from e

    def _send_http_request(
        self,
        method: str,
        url: str,
        body: Optional[Union[dict, str]] = None,
        headers: Optional[dict] = None,
    ) -> Optional[dict]:
        """
        Send an HTTP request to the Confluence server.

        Parameters:
        - method (str): The HTTP method (e.g., "GET", "POST").
        - url (str): The URL for the request.
        - body (Optional[Union[dict, str]]): The request body (default is None).
        - headers (Optional[dict]): The request headers (default is None).

        Returns:
        - Optional[dict]: The JSON response from the server, or None if the request failed.

        Raises:
        - RuntimeError: If the connection to the Confluence server is not established.
        - RuntimeError: If the HTTP request fails.
        """
        if not self._http_connection:
            raise RuntimeError("Connection to Confluence server not established.")

        headers = headers or {}
        headers.update(self._auth_headers)

        # Mask sensitive headers like the authorization token in logs
        sanitized_headers = {
            key: (value if key != "Authorization" else "REDACTED")
            for key, value in headers.items()
        }

        if body:
            headers["Content-Type"] = "application/json"
            if isinstance(body, dict):
                body = json.dumps(body)

        logger.debug(
            f"Sending {method} request to {url} with headers {sanitized_headers} and body {body}."
        )
        try:
            self._http_connection.request(method=method, url=url, body=body, headers=headers)
            response = self._http_connection.getresponse()
            response_data = response.read().decode("utf-8")

            if 200 <= response.status < 300:
                logger.debug(
                    f"{method} request to {url} successful. Status: {response.status}"
                )
                return json.loads(response_data) if response_data else None
            else:
                # Log the full response body for debugging
                logger.warning(
                    f"{method} request to {url} failed. "
                    f"Status: {response.status}, Reason: {response.reason}, Response: {response_data}"
                )
                return None
        except (http.client.HTTPException, ValueError, json.JSONDecodeError) as e:
            logger.error(f"Error during {method} request to {url}, error: {e}")
            raise RuntimeError("Failed to complete HTTP request.") from e

    def _fetch_page_metadata(self, page_id: str) -> Optional[dict]:
        """
        Fetch metadata for a Confluence page by its ID.

        Parameters:
        - page_id (str): The ID of the page to fetch metadata for.

        Returns:
        - Optional[dict]: The metadata for the page as a dictionary.
        """
        url = f"/wiki/rest/api/content/{page_id}?expand=version"
        return self._send_http_request(method="GET", url=url)

    def _fetch_page_storage_html(self, page_id: str) -> Optional[str]:
        """
        Fetch the storage format (HTML representation) of a Confluence page by its ID.

        Parameters:
        - page_id (str): The ID of the page to fetch.

        Returns:
        - Optional[str]: The HTML content of the page in storage format, or None if not found.
        """
        url = f"/wiki/rest/api/content/{page_id}?expand=body.storage"
        response = self._send_http_request(method="GET", url=url)
        return (
            response.get("body", {}).get("storage", {}).get("value")
            if response
            else None
        )

    def _convert_dict_to_html_table(self, data_dict: dict) -> str:
        """
        Convert a dictionary into an HTML table.

        Parameters:
        - data_dict (dict): The dictionary to convert into an HTML table.

        Returns:
        - str: The HTML string representing the dictionary as a table.
        """
        html = "<html><body>"
        if self._html_header:
            html += self._html_header
        html += "<table border='1'>"
        html += f"<tr><th>{self._html_table_key}</th><th>{self._html_table_value}</th></tr>"
        for key, value in data_dict.items():
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"
        html += "</table>"
        html += "</body></html>"
        return html


    def _delete_page_version(self, page_id: str, version_id: str) -> None:
        """
        Delete a specific version of a Confluence page.

        Parameters:
        - page_id (str): The ID of the page to delete.
        - version_id (str): The ID of the version to delete.
        """
        url = f"/wiki/rest/api/content/{page_id}/version/{version_id}"
        self._send_http_request(method="DELETE", url=url)


    def _update_page_storage_html(self, page_id: str, html_content: str) -> None:
        """
        Update the storage format (HTML representation) of a Confluence page by its ID.

        Parameters:
        - page_id (str): The ID of the page to update.
        - html_content (str): The new HTML content to set on the page.
        """
        url = f"/wiki/rest/api/content/{page_id}"
        metadata = self._fetch_page_metadata(page_id=page_id)
        
        if not self._html_title:
            self._html_title = metadata["title"]
        
        if metadata:
            body = {
                "version": {"number": metadata["version"]["number"] + 1},
                "type": metadata["type"],
                "title": self._html_title,
                "body": {
                    "storage": {"value": html_content, "representation": "storage"}
                },
            }
            self._send_http_request(method="PUT", url=url, body=body)
            self._delete_page_version(page_id=page_id, version_id=metadata["version"]["number"])

    def fetchall(self, page_id: Optional[str] = None) -> Optional[dict]:
        """
        Fetch the storage format (HTML representation) of a Confluence page by its ID.
        Returns a dictionary of key-value pairs extracted from the page content.

        Parameters:
        - page_id (str): The ID of the page to fetch.

        Returns:
        - Optional[dict]: A dictionary of key-value pairs from the page content, or None if not found.
        """
        if not page_id:
            page_id = self.page_id

        html = self._fetch_page_storage_html(page_id=page_id)
        if html:
            pattern = r"<tr><td>(.*?)</td><td>(.*?)</td></tr>"
            matches = re.findall(pattern=pattern, string=html)
            return {key.strip(): value.strip() for key, value in matches}
        return None

    def replaceall(self, data: dict, page_id: Optional[str] = None) -> None:
        """
        Convert a dictionary to HTML and update the storage format of a Confluence page.

        Parameters:
        - data (dict): A dictionary containing the data to set on the page.
        - page_id (str): The ID of the page to update.
        """
        if not page_id:
            page_id = self.page_id

        html = self._convert_dict_to_html_table(data_dict=data)
        self._update_page_storage_html(page_id=page_id, html_content=html)

    def search(self, query: str, ok_if_missing: bool = False, page_id: Optional[str] = None) -> str:
        """
        Fetch the storage format (HTML representation) of a Confluence page by its ID.
        Query the page for a specific key and return the corresponding value.

        Parameters:
        - query (str): The key to search for in the page.
        - page_id (str): The ID of the page to search.
        
        Returns:
        - str: The value corresponding to the queried key.
        """
        if not page_id:
            page_id = self.page_id

        try:
            res = self.fetchall(page_id=page_id)[query]
            logger.debug(f"Search result for key '{query}': {res}")
        except KeyError:
            if not ok_if_missing:
                raise ValueError(f"Key '{query}' not found in {page_id} page.")
            res = None
        return res

    def insert(self, key: str, value: str, page_id: Optional[str] = None) -> None:
        """
        Insert a new key-value pair into the storage format of a Confluence page.

        Parameters:
        - page_id (str): The ID of the page to update.
        - key (str): The key to insert.
        - value (str): The value to insert.

        Raises:
        - ValueError: If the key already exists in the page.
        """
        if not page_id:
            page_id = self.page_id

        data = self.fetchall(page_id=page_id)
        if key in data:
            raise ValueError(f"Key '{key}' already exists in the page.")
        data[key] = value
        self.replaceall(data=data, page_id=page_id)

    def delete(self, key: str, ok_if_missing: bool = False, page_id: Optional[str] = None) -> None:
        """
        Delete a key-value pair from the storage format of a Confluence page.

        Parameters:
        - key (str): The key to delete.
        - ok_if_missing (bool): If True, do not raise an error if the key is not found.
        - page_id (str): The ID of the page to update.

        Raises:
        - ValueError: If the key doesn't exist in the page.
        """
        if not page_id:
            page_id = self.page_id

        data = self.fetchall(page_id=page_id)
        if key not in data:
            if not ok_if_missing:
                raise ValueError(f"Key '{key}' does not exist in the page.")
            return None  # Key not found and that's OK
        del data[key]  
        self.replaceall(data=data, page_id=page_id)

    def replace(self, key: str, value: str, ok_if_missing: bool = False, page_id: Optional[str] = None) -> None:
        """
        Update a key-value pair in the storage format of a Confluence page.

        Parameters:
        - key (str): The key to update.
        - value (str): The new value to set.
        - ok_if_missing (bool): If True, do not raise an error if the key is not found.
        - page_id (str): The ID of the page to update.
        """
        if not page_id:
            page_id = self.page_id

        data = self.fetchall(page_id=page_id)
        if key not in data:
            if not ok_if_missing:
                raise ValueError(f"Key '{key}' does not exist in the page.")
            return None  # Key not found and that's OK
        data[key] = value
        self.replaceall(page_id=page_id, data=data)

    def upsert(self, key: str, value: str, page_id: Optional[str] = None) -> None:
        """
        Update or insert a key-value pair in the storage format of a Confluence page.

        Parameters:
        - key (str): The key to upsert.
        - value (str): The value to set.
        - page_id (str): The ID of the page to update.
        """
        if not page_id:
            page_id = self.page_id

        data = self.fetchall(page_id=page_id)
        data[key] = value
        self.replaceall(data=data, page_id=page_id)

    def close(self):
        """
        Close the connection to the Confluence server.
        """
        if self._http_connection:
            try:
                self._http_connection.close()
                logger.debug("Disconnected from Confluence server.")
            except OSError as e:
                logger.error(f"Error while disconnecting: {e}")
            finally:
                self._http_connection = None

    def __enter__(self) -> "PageManager":
        """
        Enter the runtime context related to this object.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context and clean up resources.
        """
        self.close()
        if exc_type:
            logger.error(f"Exception occurred: {exc_type}, {exc_value}")
        return False  # Propagate exceptions
