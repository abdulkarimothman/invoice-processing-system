from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from invoice_automation.dto.attachment_dto import EmailAttachmentDTO


class ProcessedEmailDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    message_id: str = Field(min_length=1)
    sender: str = Field(min_length=1)
    subject: str
    body: str
    received_at: datetime
    attachments: list[EmailAttachmentDTO] = Field(default_factory=list)
