from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from dsp2_client.models.type_aliases import CurrencyCode, NonEmptyStr


class AccountType(str, Enum):
    CACC = "CACC"  # Cash Account
    CARD = "CARD"  # Card Account


class AccountUsage(str, Enum):
    PRIV = "PRIV"  # Private account
    ORGA = "ORGA"  # Pro account


AccountID = Annotated[str, Field(pattern=r"^acct_[a-zA-Z0-9]{24}$")]
IBAN = Annotated[str, Field(min_length=15, max_length=34)]


class AccountSchema(BaseModel):
    """
    Account schema matching OpenAPI spec.
    """

    id: AccountID
    type: AccountType
    usage: AccountUsage
    iban: IBAN
    name: NonEmptyStr
    currency: CurrencyCode

    @field_validator("iban")
    def iban_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("IBAN must be alphanumeric")
        return v.upper()
