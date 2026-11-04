import pytest
from pydantic import ValidationError

from invoice_automation.dto.attachment_dto import (
    AttachmentStatus,
    EmailAttachmentDTO,
)


def test_create_valid_pdf_attachment():
    attachment = EmailAttachmentDTO(
        filename="invoice.pdf",
        content_type="application/pdf",
        size_bytes=1024,
        content=b"%PDF-1.7",
        processing_status=AttachmentStatus.READY,
    )

    assert attachment.filename == "invoice.pdf"
    assert attachment.content_type == "application/pdf"
    assert attachment.size_bytes == 1024
    assert attachment.content == b"%PDF-1.7"
    assert attachment.processing_status == AttachmentStatus.READY


def test_attachment_status_defaults_to_pending():
    attachment = EmailAttachmentDTO(
        filename="invoice.pdf",
        content_type="application/pdf",
        size_bytes=1024,
    )

    assert attachment.processing_status == AttachmentStatus.PENDING


def test_empty_filename_is_rejected():
    with pytest.raises(ValidationError):
        EmailAttachmentDTO(
            filename="",
            content_type="application/pdf",
            size_bytes=1024,
        )


def test_negative_file_size_is_rejected():
    with pytest.raises(ValidationError):
        EmailAttachmentDTO(
            filename="invoice.pdf",
            content_type="application/pdf",
            size_bytes=-1,
        )


def test_attachment_can_have_no_content():
    attachment = EmailAttachmentDTO(
        filename="document.docx",
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        size_bytes=2048,
        processing_status=AttachmentStatus.UNSUPPORTED,
    )

    assert attachment.content is None
