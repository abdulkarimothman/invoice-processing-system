from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from invoice_automation.schemas.invoice import (
    InvoiceData,
    PaymentStatus,
)


def test_create_valid_invoice():
    invoice = InvoiceData(
        vendor_name="ABC GmbH",
        invoice_number="INV-2026-1042",
        invoice_date="2026-10-25",
        total_amount=Decimal("1190.00"),
        currency="EUR",
        payment_status=PaymentStatus.PAID,
    )

    assert invoice.vendor_name == "ABC GmbH"
    assert invoice.total_amount == Decimal("1190.00")
    assert invoice.invoice_date == date(2026, 10, 25)


def test_missing_currency_defaults_to_none():
    invoice = InvoiceData()

    assert invoice.currency is None


@pytest.mark.parametrize(
    "currency",
    ["EU", "EURO", "EUROO"],
)
def test_invalid_currency_length(currency):
    with pytest.raises(ValidationError):
        InvoiceData(currency=currency)


def test_missing_payment_status_defaults_to_unknown():
    invoice = InvoiceData()

    assert invoice.payment_status == PaymentStatus.UNKNOWN
