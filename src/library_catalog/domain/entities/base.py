from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseEntity:
    uuid: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now(UTC))
    updated_at: datetime | None = None
