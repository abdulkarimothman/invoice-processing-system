import pytest

from invoice_automation.services.email_processor import EmailProcessor


def test_attachment_size_below_limit():
    size_bytes = 5 * 1024 * 1024

    assert EmailProcessor.validate_attachment_size(size_bytes) is True


def test_attachment_size_at_limit():
    size_bytes = 15 * 1024 * 1024

    assert EmailProcessor.validate_attachment_size(size_bytes) is True


def test_attachment_size_above_limit():
    size_bytes = 20 * 1024 * 1024

    assert EmailProcessor.validate_attachment_size(size_bytes) is False


@pytest.mark.parametrize(
    "content_type",
    [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "image/png",
        "image/jpeg",
    ],
)
def test_supported_attachment_types(content_type):
    assert EmailProcessor.validate_attachment_type(content_type) is True


def test_unsupported_attachment_type():
    assert EmailProcessor.validate_attachment_type("application/zip") is False
