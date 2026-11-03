from decimal import Decimal

from invoice_automation.schemas.invoice import InvoiceData
from invoice_automation.services.invoice_validator import validate_invoice


def test_missing_required_fields_require_human_review():
    invoice = InvoiceData()

    validated_invoice = validate_invoice(invoice)

    assert validated_invoice.requires_human_review is True
    assert len(validated_invoice.review_reasons) == 4


def test_complete_invoice_does_not_require_human_review():
    invoice = InvoiceData(
        vendor_name="ABC GmbH",
        invoice_number="INV-2026-1042",
        invoice_date="2026-10-25",
        total_amount=Decimal("1190.00"),
    )

    validated_invoice = validate_invoice(invoice)

    assert validated_invoice.requires_human_review is False
    assert validated_invoice.review_reasons == []


def test_validation_does_not_modify_original_invoice():
    invoice = InvoiceData()

    validated_invoice = validate_invoice(invoice)

    assert invoice.requires_human_review is False
    assert invoice.review_reasons == []

    assert validated_invoice.requires_human_review is True
    assert validated_invoice is not invoice


def test_review_reasons_identify_missing_fields():
    invoice = InvoiceData(
        vendor_name="ABC GmbH",
        total_amount=Decimal("1190.00"),
    )

    validated_invoice = validate_invoice(invoice)

    assert "Missing required field: invoice_number" in validated_invoice.review_reasons
    assert "Missing required field: invoice_date" in validated_invoice.review_reasons