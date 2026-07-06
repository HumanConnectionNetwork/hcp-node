from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class HumanitarianRecord:
    reported_name: str
    estimated_age: str
    reported_location: str
    event_type: str
    status: str
    source: str
    description: str

    record_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    protocol_version: str = "0.1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def validate(self) -> list[str]:
        errors: list[str] = []

        required_fields = {
            "reported_name": self.reported_name,
            "reported_location": self.reported_location,
            "event_type": self.event_type,
            "status": self.status,
            "source": self.source,
        }

        for field_name, value in required_fields.items():
            if not value or not str(value).strip():
                errors.append(f"{field_name} is required")

        if self.description and len(self.description) > 500:
            errors.append("description must be 500 characters or less")

        return errors

    def is_valid(self) -> bool:
        return len(self.validate()) == 0

    def missing_fields(self) -> list[str]:
        return [
            field_name
            for field_name, value in self.to_dict().items()
            if value is None or str(value).strip() == ""
        ]

    def to_hcp_payload(self) -> dict[str, Any]:
        return {
            "protocol": "HCP",
            "protocol_version": self.protocol_version,
            "type": "humanitarian_record",
            "record": self.to_dict(),
        }

    def to_json(self) -> dict[str, Any]:
        return self.to_hcp_payload()
