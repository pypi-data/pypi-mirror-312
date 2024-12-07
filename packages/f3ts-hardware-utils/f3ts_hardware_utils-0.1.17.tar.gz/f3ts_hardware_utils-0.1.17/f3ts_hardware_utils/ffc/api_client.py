"""F3TS Plugin Utilities."""
import logging
import os

import requests
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class FixtureCNTLAPIClient:
    """F3TS Pytest F3TS Webservice API.

    Object for creating and sending requests to the Test runner backend
    """

    def __init__(
        self,
        api_url: str = os.getenv("PYTEST_API_URL", "pytest-f3ts-api:8886"),
        api_str: str = os.getenv("FFC_API_STR", "/api/v1/hardware/ffc"),
    ):
        """Initialize the F3TS Backend API.

        Store the API URL and number of request retries. A request will be
        retried for the provided number of retries. If it continues to fail,
        an exception will be raised.
        """
        self.api_prefix = f"{api_url}{api_str}"
        self.retries = 3
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_fixture_close(self):
        """Get operator id from run information stored in database"""
        attempt = 0
        status_code = 500
        error_msg = ""
        while attempt < self.retries:
            response = requests.get(
                f"{self.api_prefix}/get_close_state",
                headers=self.headers,
                verify=False,
            )

            if response.status_code == 200:
                return bool(response.json())
            else:
                status_code = response.status_code
                error_msg = response.json()

            attempt += 1

        raise HTTPException(
            status_code,
            f"Unable to access fixture controller, {error_msg}",
        )
