class EmailProcessor:
    MAX_ATTACHMENT_SIZE = 15 * 1024 * 1024

    SUPPORTED_CONTENT_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "image/png",
        "image/jpeg",
    }

    @classmethod
    def validate_attachment_size(cls, size_bytes: int) -> bool:
        return size_bytes <= cls.MAX_ATTACHMENT_SIZE

    @classmethod
    def validate_attachment_type(cls, content_type: str) -> bool:
        return content_type in cls.SUPPORTED_CONTENT_TYPES
