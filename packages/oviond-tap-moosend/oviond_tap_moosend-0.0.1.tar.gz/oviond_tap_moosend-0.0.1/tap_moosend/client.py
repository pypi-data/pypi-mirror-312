from __future__ import annotations
import typing as t
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class MoosendStream(RESTStream):
    """Moosend stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root."""
        return "https://api.moosend.com/v3"

    def get_url_params(
        self, context: Context | None, next_page_token: t.Any | None
    ) -> dict[str, t.Any]:
        """Return query parameters for the API request."""
        page = next_page_token.get("page", 1) if next_page_token else 1
        page_size = next_page_token.get("page_size", 1000) if next_page_token else 1000
        return {
            "apikey": self.config["api_token"],
            "page": page,
            "pageSize": page_size,
        }

    def prepare_request_headers(self, context: Context | None) -> dict[str, str]:
        """Prepare headers for the HTTP request."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_next_page_token(
        self, response: requests.Response, previous_token: t.Any | None
    ) -> t.Optional[dict]:
        """Extract the next page token."""
        paging_info = response.json().get("Context", {}).get("Paging", {})

        current_page = paging_info.get("CurrentPage", 1)
        total_pages = paging_info.get("TotalPageCount", 1)
        page_size = paging_info.get("PageSize", 1000)

        if current_page <= total_pages:
            return {"page": current_page + 1, "page_size": page_size}

        return None

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and yield result records."""
        data = response.json()
        api_token = self.config["api_token"]

        records = list(extract_jsonpath(self.records_jsonpath, input=data))
        for record in records:
            yield {**record, "profile_id": api_token}
