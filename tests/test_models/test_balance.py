import pytest
from pydantic import ValidationError

from dsp2_client.models.balance import BalanceSchema


@pytest.mark.parametrize(
    "data, should_pass",
    [
        (
            {
                "id": "blnc_1234567890abcdefABCDEF12",
                "name": "Balance1",
                "amount": 500,
                "currency": "USD",
                "type": "VALU",
            },
            True,
        ),
        (
            {
                "id": "blnc_invalid",
                "name": "",
                "amount": -10,
                "currency": None,
                "type": "CLBD",
            },
            False,
        ),
    ],
)
def test_balance_schema(data, should_pass):
    if should_pass:
        model = BalanceSchema(**data)
        assert model.id.startswith("blnc")
    else:
        with pytest.raises(ValidationError):
            BalanceSchema(**data)
