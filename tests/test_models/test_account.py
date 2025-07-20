import pytest
from pydantic import ValidationError

from dsp2_client.models.account import AccountSchema


@pytest.mark.parametrize(
    "data, should_pass",
    [
        (
            {
                "id": "acct_x05RAIZbtzKCUJ7m1MEnzOI5",
                "type": "CACC",
                "usage": "PRIV",
                "iban": "IBAN12345678901234",
                "name": "Account1",
                "currency": "EUR",
            },
            True,
        ),
        (
            {
                "id": "acct_short",
                "type": "CARD",
                "usage": "ORGA",
                "iban": "INVALID!IBAN",
                "name": "Account2",
                "currency": "EUR",
            },
            False,
        ),
        (
            {
                "id": "acct_x05RAIZbtzKCUJ7m1MEnzOI5",
                "type": "UNKNOWN",
                "usage": "PRIV",
                "iban": "IBAN12345678901234",
                "name": "Account3",
                "currency": "EUR",
            },
            False,
        ),
    ],
)
def test_account_schema(data, should_pass):
    if should_pass:
        model = AccountSchema(**data)
        assert model.id.startswith("acct_")
        assert model.iban.isalnum()
    else:
        with pytest.raises(ValidationError):
            AccountSchema(**data)


def test_iban_uppercase(valid_account):
    valid_account["iban"] = "ibanlowercase123"
    model = AccountSchema(**valid_account)
    assert model.iban.isupper()
