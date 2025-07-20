from datetime import datetime

import pytest
from pydantic import ValidationError

from dsp2_client.models.transaction import TransactionSchema


@pytest.mark.parametrize(
    "data, should_pass",
    [
        (
            {
                "id": "tran_1234567890abcdefABCDEF12",
                "label": "Test Transaction",
                "amount": 123,
                "crdt_dbit_indicator": "CRDT",
                "status": "BOOK",
                "currency": "EUR",
                "date_operation": "2024-01-01T10:00:00Z",
                "date_processed": "2024-01-02T12:00:00Z",
            },
            True,
        ),
        (
            {
                "id": "tran_wrongid",
                "label": "",
                "amount": 0,
                "crdt_dbit_indicator": "INVALID",
                "status": "INVALID",
                "currency": None,
                "date_operation": "not-a-date",
                "date_processed": None,
            },
            False,
        ),
    ],
)
def test_transaction_schema(data, should_pass):
    if should_pass:
        model = TransactionSchema(**data)
        assert isinstance(model.date_operation, datetime)
    else:
        with pytest.raises(ValidationError):
            TransactionSchema(**data)
