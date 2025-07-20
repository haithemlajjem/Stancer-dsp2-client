from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from dsp2_client.models.type_aliases import CurrencyCode, NonEmptyStr


class BalanceType(str, Enum):
    CLBD = "CLBD"  # ClosingBooked
    XPCD = "XPCD"  # Expected
    VALU = "VALU"  # Value-date balance
    ITAV = "ITAV"  # InterimAvailable
    PRCD = "PRCD"  # PreviouslyClosedBooked
    OTHR = "OTHR"  # Other Balance


BalanceID = Annotated[str, Field(pattern=r"^blnc_[a-zA-Z0-9]{24}$")]


class BalanceSchema(BaseModel):
    """
    Balance schema matching OpenAPI spec.
    """

    id: BalanceID
    name: NonEmptyStr
    amount: int
    currency: Optional[CurrencyCode]
    type: BalanceType
