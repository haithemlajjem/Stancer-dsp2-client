import pytest

from dsp2_client.models import (
    AccountSchema,
    BalanceSchema,
    TransactionSchema,
    UserIdentitySchema,
)


def test_user_identity_schema_valid():
    """
    Test that UserIdentitySchema can be instantiated with valid data
    and the 'id' field is correctly set.
    """
    data = {
        "id": "user_TLMLiOYdrPdO7YYuuLdK9Dvw",
        "prefix": "DOCT",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
    }
    model = UserIdentitySchema(**data)
    assert model.id == "user_TLMLiOYdrPdO7YYuuLdK9Dvw"


def test_account_schema_valid():
    """
    Test that AccountSchema accepts valid input and correctly sets the 'type' field.
    """
    data = {
        "id": "acct_x05RAIZbtzKCUJ7m1MEnzOI5",
        "type": "CACC",
        "usage": "PRIV",
        "iban": "iban123",
        "name": "Test Account",
        "currency": "EUR",
    }
    model = AccountSchema(**data)
    assert model.type == "CACC"


def test_balance_schema_valid():
    """
    Test that BalanceSchema can be instantiated with valid data and
    the 'amount' is correct.
    """
    data = {
        "id": "blnc_Q1v8cWPhNZTAx1XideNDYU9e",
        "name": "Balance",
        "amount": 1000,
        "currency": "EUR",
        "type": "CLBD",
    }
    model = BalanceSchema(**data)
    assert model.amount == 1000


def test_transaction_schema_valid():
    """
    Test that TransactionSchema handles a complete valid transaction,
    including optional and datetime fields.
    """
    data = {
        "id": "tran_s5yue7V0vorTv1DZpCxi8Mtk",
        "label": "Test txn",
        "amount": 100,
        "crdt_dbit_indicator": "CRDT",
        "status": "BOOK",
        "currency": "EUR",
        "date_operation": "2023-01-01T12:00:00",
        "date_processed": None,
    }
    model = TransactionSchema(**data)
    assert model.label == "Test txn"
