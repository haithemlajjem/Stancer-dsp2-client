"""
models.py

This module defines Pydantic data models that represent the structure of
API responses.

The models cover:
- User identity information
- Bank account details
- Account balances
- Account transactions

"""

from datetime import date, datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel


# Identity
class UserIdentitySchema(BaseModel):
    id: str
    prefix: Literal["DOCT", "MADM", "MISS", "MIST"]
    first_name: str
    last_name: str
    date_of_birth: date


# Account
class AccountType(str, Enum):
    CACC = "CACC"  # Cash Account
    CARD = "CARD"  # Card Account


class AccountUsage(str, Enum):
    PRIV = "PRIV"  # Private account
    ORGA = "ORGA"  # Pro account


class AccountSchema(BaseModel):
    id: str
    type: AccountType
    usage: AccountUsage
    iban: str
    name: str
    currency: str


# Balance
class BalanceType(str, Enum):
    CLBD = "CLBD"  # ClosingBooked
    XPCD = "XPCD"  # Expected
    VALU = "VALU"  # Value-date balance
    ITAV = "ITAV"  # InterimAvailable
    PRCD = "PRCD"  # PreviouslyClosedBooked
    OTHR = "OTHR"  # Other Balance


class BalanceSchema(BaseModel):
    id: str
    name: str
    amount: int
    currency: Optional[str]  # nullable in schema
    type: BalanceType


# Transaction
class TransactionCreditDebitIndicator(str, Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


class TransactionStatus(str, Enum):
    BOOK = "BOOK"
    PDNG = "PDNG"
    FUTR = "FUTR"
    INFO = "INFO"


class TransactionSchema(BaseModel):
    id: str
    label: str
    amount: int
    crdt_dbit_indicator: TransactionCreditDebitIndicator
    status: TransactionStatus
    currency: Optional[str]
    date_operation: datetime
    date_processed: Optional[datetime]
