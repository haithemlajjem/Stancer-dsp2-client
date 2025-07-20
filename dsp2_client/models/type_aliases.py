from typing import Annotated

from pydantic import Field

NonEmptyStr = Annotated[str, Field(min_length=1)]
CurrencyCode = Annotated[str, Field(min_length=3, max_length=3)]
