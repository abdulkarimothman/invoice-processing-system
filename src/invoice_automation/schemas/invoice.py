from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PaymentStatus(StrEnum):
    PAID = "paid"
    UNPAID = "unpaid"
    PARTIALLY_PAID = "partially_paid"
    UNKNOWN = "unknown"


class InvoiceData(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    vendor_name: str | None = Field(default=None, min_length=1)
    invoice_number: str | None = Field(default=None, min_length=1)
    invoice_date: date | None = None

    total_amount: Decimal | None = Field(default=None, ge=0)

    currency: str | None = Field(default=None, min_length=3, max_length=3)

    payment_status: PaymentStatus = PaymentStatus.UNKNOWN
    payment_method: str | None = None

    requires_human_review: bool = False
    review_reasons: list[str] = Field(default_factory=list)
