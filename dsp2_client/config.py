"""
Loads DSP2 API configuration from environment variables defined in a .env
"""

import os

from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://dsp2-technical-test.iliad78.net")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT", "/oauth/token")
