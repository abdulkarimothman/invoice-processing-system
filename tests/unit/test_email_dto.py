from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from invoice_automation.dto.email_dto import ProcessedEmailDTO


def test_create_valid_email():
    received_at = datetime.now(UTC)

    email = ProcessedEmailDTO(
        message_id="message-123",
        sender="accounting@company.com",
        subject="Invoice December 2026",
        body="Please find the attached invoice.",
        received_at=received_at,
    )

    assert email.message_id == "message-123"
    assert email.sender == "accounting@company.com"
    assert email.subject == "Invoice December 2026"
    assert email.body == "Please find the attached invoice."
    assert email.received_at == received_at
    assert email.attachments == []


def test_email_can_have_empty_subject_and_body():
    email = ProcessedEmailDTO(
        message_id="message-123",
        sender="accounting@company.com",
        subject="",
        body="",
        received_at=datetime.now(UTC),
    )

    assert email.subject == ""
    assert email.body == ""


def test_email_can_contain_attachments():
    email = ProcessedEmailDTO(
        message_id="message-123",
        sender="accounting@company.com",
        subject="Invoice",
        body="See attached file.",
        received_at=datetime.now(UTC),
        attachments=[
            {
                "filename": "invoice.pdf",
                "content_type": "application/pdf",
                "size_bytes": 1024,
            }
        ],
    )

    assert len(email.attachments) == 1
    assert email.attachments[0].filename == "invoice.pdf"


@pytest.mark.parametrize("field", ["message_id", "sender"])
def test_required_identifiers_cannot_be_empty(field):
    email_data = {
        "message_id": "message-123",
        "sender": "accounting@company.com",
        "subject": "Invoice",
        "body": "Invoice attached.",
        "received_at": datetime.now(UTC),
    }

    email_data[field] = ""

    with pytest.raises(ValidationError):
        ProcessedEmailDTO(**email_data)


def test_each_email_has_an_independent_attachment_list():
    first_email = ProcessedEmailDTO(
        message_id="message-1",
        sender="first@company.com",
        subject="First",
        body="",
        received_at=datetime.now(UTC),
    )

    second_email = ProcessedEmailDTO(
        message_id="message-2",
        sender="second@company.com",
        subject="Second",
        body="",
        received_at=datetime.now(UTC),
    )

    first_email.attachments.append(
        {
            "filename": "invoice.pdf",
            "content_type": "application/pdf",
            "size_bytes": 1024,
        }
    )

    assert len(first_email.attachments) == 1
    assert len(second_email.attachments) == 0
