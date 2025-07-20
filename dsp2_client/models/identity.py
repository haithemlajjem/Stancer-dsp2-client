from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from dsp2_client.models.type_aliases import NonEmptyStr

IdentityID = Annotated[str, Field(pattern=r"^user_[a-zA-Z0-9]{24}$")]


class UserIdentitySchema(BaseModel):
    """
    User identity schema, matching OpenAPI spec.
    """

    id: IdentityID
    prefix: Literal["DOCT", "MADM", "MISS", "MIST"]
    first_name: NonEmptyStr
    last_name: NonEmptyStr
    date_of_birth: date
