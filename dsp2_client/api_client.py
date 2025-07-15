"""
DSP2Client: A client library for interacting with a STET-compliant DSP2 API.
Handles authentication and requests for identity, accounts, balances, and transactions.
"""

from typing import List, Optional

import httpx

from . import config, logger
from .models import AccountSchema, BalanceSchema, TransactionSchema, UserIdentitySchema


class DSP2Client:
    def __init__(self, username: str, password: str, base_url: Optional[str] = None):
        """
        Initialize the DSP2Client with optional username, password, and base_url.
        Falls back to environment config if parameters are not provided.
        """
        if not username or not password:
            raise ValueError("Username and password must be provided via parameters")
        self.username = username
        self.password = password

        # Use custom base_url if provided; otherwise fall back to config default
        self.base_url = base_url or config.API_BASE_URL
        self._token: Optional[str] = None

        # Create an HTTPX client for persistent connection reuse
        self._client = httpx.Client(base_url=self.base_url)

        logger.logger.info(f"DSP2Client initialized for user {self.username}")

        # Authenticate the user to get the access token
        self.authenticate()

    def authenticate(self) -> None:
        """
        Authenticate using username and password and store the bearer token.
        """
        token_url = config.TOKEN_ENDPOINT

        # Request payload as per OAuth2 Resource Owner Password Credentials Grant
        payload = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "stet",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            # Send POST request to obtain access token
            response = self._client.post(token_url, data=payload, headers=headers)

            response.raise_for_status()  # Raise exception for HTTP errors
            token_data = response.json()
            self._token = token_data.get("access_token")
            if not self._token:
                raise RuntimeError("Failed to obtain access token")

            # Add Authorization header to all subsequent requests
            self._client.headers.update({"Authorization": f"Bearer {self._token}"})
            logger.logger.info("Authentication successful")
        except httpx.HTTPStatusError as e:
            logger.logger.error(f"HTTP error during authentication: {e.response.text}")
            raise RuntimeError("Authentication failed") from e
        except Exception as e:
            logger.logger.error(f"Unexpected error during authentication: {e}")
            raise RuntimeError("Authentication failed") from e

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Internal method to perform a GET request.
        """
        try:
            logger.logger.debug(f"GET {endpoint} with params={params}")
            response = self._client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.logger.error(f"HTTP error on GET {endpoint}: {e.response.text}")
            raise RuntimeError(f"Failed GET {endpoint}") from e
        except Exception as e:
            logger.logger.error(f"Unexpected error on GET {endpoint}: {e}")
            raise RuntimeError(f"Failed GET {endpoint}") from e

    def get_identity(self) -> UserIdentitySchema:
        """
        Retrieve the identity information of the authenticated user.
        """
        data = self._get("/stet/identity")
        return UserIdentitySchema(**data)

    def get_accounts(self) -> List[AccountSchema]:
        """
        Retrieve a list of user accounts.
        """
        data = self._get("/stet/account")
        return [AccountSchema(**item) for item in data]

    def get_account(self, account_id: str) -> AccountSchema:
        """
        Retrieve a single account by ID.
        """
        data = self._get(f"/stet/account/{account_id}")
        return AccountSchema(**data)

    def get_balances(self, account_id: str) -> List[BalanceSchema]:
        """
        Retrieve balances for a given account ID.
        """
        data = self._get(f"/stet/account/{account_id}/balance")
        return [BalanceSchema(**item) for item in data]

    def get_transactions(
        self, account_id: str, page: int = 1, count: int = 10
    ) -> List[TransactionSchema]:
        """
        Retrieve paginated list of transactions for an account.
        """
        params = {"page": page, "count": count}
        data = self._get(f"/stet/account/{account_id}/transaction", params=params)
        return [TransactionSchema(**item) for item in data]

    def get_full_user_data(self, transactions_per_account: int = 10) -> dict:
        """
        Retrieve and return all DSP2 user data:
        - Identity
        - Accounts
        - Balances (per account)
        - Transactions (per account)

        :param transactions_per_account: Number of transactions to retrieve per account
        :return: Dictionary with all data formatted and grouped
        """
        identity = self.get_identity()
        accounts = self.get_accounts()

        full_data = {
            "identity": identity.dict(),
            "accounts": [],
        }
        # Iterate through each account and enrich it with balances and transactions
        for account in accounts:
            account_data = account.dict()

            # Add balances and transactions to each account
            balances = self.get_balances(account.id)
            transactions = self.get_transactions(
                account.id, count=transactions_per_account
            )

            account_data["balances"] = [balance.dict() for balance in balances]
            account_data["transactions"] = [txn.dict() for txn in transactions]

            # Append complete account info to the result list
            full_data["accounts"].append(account_data)

        return full_data
