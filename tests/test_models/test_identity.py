import pytest
from pydantic import ValidationError

from dsp2_client.models.identity import UserIdentitySchema


@pytest.mark.parametrize(
    "data, should_pass",
    [
        (
            {
                "id": "user_123456789012345678901234",
                "prefix": "DOCT",
                "first_name": "A",
                "last_name": "B",
                "date_of_birth": "2000-01-01",
            },
            True,
        ),
        (
            {
                "id": "wrongprefix_123",
                "prefix": "DOCT",
                "first_name": "A",
                "last_name": "B",
                "date_of_birth": "2000-01-01",
            },
            False,
        ),
        (
            {
                "id": "user_123456789012345678901234",
                "prefix": "INVALID",
                "first_name": "A",
                "last_name": "B",
                "date_of_birth": "2000-01-01",
            },
            False,
        ),
        (
            {
                "id": "user_123456789012345678901234",
                "prefix": "DOCT",
                "first_name": "",
                "last_name": "B",
                "date_of_birth": "2000-01-01",
            },
            False,
        ),
    ],
)
def test_user_identity_schema(data, should_pass):
    if should_pass:
        model = UserIdentitySchema(**data)
        assert model.id.startswith("user_")
    else:
        with pytest.raises(ValidationError):
            UserIdentitySchema(**data)
