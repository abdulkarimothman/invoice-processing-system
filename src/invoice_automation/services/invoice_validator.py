from invoice_automation.schemas.invoice import InvoiceData


REQUIRED_FIELDS = (
    "vendor_name",
    "invoice_number",
    "invoice_date",
    "total_amount",
)


def validate_invoice(invoice: InvoiceData) -> InvoiceData:
    review_reasons = list(invoice.review_reasons)

    for field_name in REQUIRED_FIELDS:
        field_value = getattr(invoice, field_name)

        if field_value is None:
            reason = f"Missing required field: {field_name}"

            if reason not in review_reasons:
                review_reasons.append(reason)

    requires_human_review = (
        invoice.requires_human_review or bool(review_reasons)
    )

    return invoice.model_copy(
        update={
            "requires_human_review": requires_human_review,
            "review_reasons": review_reasons,
        }
    )