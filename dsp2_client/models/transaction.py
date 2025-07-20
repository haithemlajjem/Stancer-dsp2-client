from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from dsp2_client.models.type_aliases import CurrencyCode, NonEmptyStr


class TransactionCreditDebitIndicator(str, Enum):
    CRDT = "CRDT"  # Credit
    DBIT = "DBIT"  # Debit


class TransactionStatus(str, Enum):
    BOOK = "BOOK"  # Booked
    PDNG = "PDNG"  # Pending
    FUTR = "FUTR"  # Future
    INFO = "INFO"  # Info


TransactionID = Annotated[str, Field(pattern=r"^tran_[a-zA-Z0-9]{24}$")]


class TransactionSchema(BaseModel):
    id: TransactionID
    label: NonEmptyStr
    amount: int
    crdt_dbit_indicator: TransactionCreditDebitIndicator
    status: TransactionStatus
    currency: Optional[CurrencyCode]
    date_operation: datetime
    date_processed: Optional[datetime]
