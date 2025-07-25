"""
Loads DSP2 API configuration from environment variables defined in a .env
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default: str) -> str:
    value = os.getenv(key)
    return value if value else default


API_BASE_URL = get_env("API_BASE_URL", "https://dsp2-technical-test.iliad78.net")
TOKEN_ENDPOINT = get_env("TOKEN_ENDPOINT", "/oauth/token")
IDENTITY = os.getenv("IDENTITY", "/stet/identity")
ACCOUNTS = os.getenv("ACCOUNTS", "/stet/account")
BALANCE = os.getenv("BALANCE", "/stet/account/{account_id}/balance")
TRANSACTIONS = os.getenv("TRANSACTIONS", "/stet/account/{account_id}/transaction")
ACCOUNT = os.getenv("ACCOUNT", "/stet/account/{account_id}")
