"""
DSP2Client: A client library for interacting with a STET-compliant DSP2 API.
Handles authentication and requests for identity, accounts, balances, and transactions.
"""

from typing import List

from dsp2_client.models.account import AccountSchema
from dsp2_client.models.balance import BalanceSchema
from dsp2_client.models.identity import UserIdentitySchema
from dsp2_client.models.transaction import TransactionSchema

from .. import config
from .authenticator import DSP2Authenticator
from .base_client import BaseAPIClient


class DSP2Client:
    def __init__(self, username: str, password: str, base_url: str | None = None):
        self.base_url = base_url or config.API_BASE_URL
        self.authenticator = DSP2Authenticator(
            username, password, BaseAPIClient(self.base_url)._client
        )

        token = self.authenticator.authenticate()
        self.api = BaseAPIClient(base_url=self.base_url, token=token)

    def ensure_authenticated(self):
        """
        Ensure the client is authenticated before making API calls.
        """
        if not self.authenticator.token:
            token = self.authenticator.authenticate()
            self.api.set_token(token)

    def get_identity(self) -> UserIdentitySchema:
        self.ensure_authenticated()
        data = self.api.get(config.IDENTITY)
        return UserIdentitySchema(**data)

    def get_accounts(self) -> List[AccountSchema]:
        self.ensure_authenticated()
        data = self.api.get(config.ACCOUNTS)
        return [AccountSchema(**item) for item in data]

    def get_account(self, account_id: str) -> AccountSchema:
        self.ensure_authenticated()
        data = self.api.get(config.ACCOUNT.format(account_id=account_id))
        return AccountSchema(**data)

    def get_balances(self, account_id: str) -> List[BalanceSchema]:
        self.ensure_authenticated()
        data = self.api.get(config.BALANCE.format(account_id=account_id))
        return [BalanceSchema(**item) for item in data]

    def get_transactions(
        self, account_id: str, page: int = 1, count: int = 10
    ) -> List[TransactionSchema]:
        self.ensure_authenticated()
        params = {"page": page, "count": count}
        data = self.api.get(
            config.TRANSACTIONS.format(account_id=account_id), params=params
        )
        return [TransactionSchema(**item) for item in data]

    def get_full_user_data(self, transactions_per_account: int = 10) -> dict:
        self.ensure_authenticated()
        identity = self.get_identity()
        accounts = self.get_accounts()

        full_data = {"identity": identity.model_dump(), "accounts": []}
        for account in accounts:
            account_data = account.model_dump()
            balances = self.get_balances(account.id)
            transactions = self.get_transactions(
                account.id, count=transactions_per_account
            )
            account_data["balances"] = [balance.model_dump() for balance in balances]
            account_data["transactions"] = [txn.model_dump() for txn in transactions]
            full_data["accounts"].append(account_data)
        return full_data
