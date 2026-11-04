from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AttachmentStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    UNSUPPORTED = "unsupported"
    TOO_LARGE = "too_large"
    DOWNLOAD_FAILED = "download_failed"
    INVALID_FILE = "invalid_file"


class EmailAttachmentDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    filename: str = Field(min_length=1)
    content_type: str
    size_bytes: int = Field(ge=0)
    content: bytes | None = None
    processing_status: AttachmentStatus = AttachmentStatus.PENDING
