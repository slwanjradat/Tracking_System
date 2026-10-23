"""Domain models for package tracking."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class PackageStatus(str, Enum):
    CREATED = "created"
    RECEIVED = "received"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"


@dataclass(frozen=True)
class TrackingEvent:
    """One recorded change in a package's journey."""

    status: PackageStatus
    location: str
    note: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Package:
    """A parcel and its chronological tracking history."""

    tracking_number: str
    recipient: str
    events: list[TrackingEvent] = field(default_factory=list)

    @property
    def current_status(self) -> PackageStatus:
        if not self.events:
            return PackageStatus.CREATED
        return self.events[-1].status

    def add_event(self, event: TrackingEvent) -> None:
        allowed_transitions = {
            PackageStatus.CREATED: {PackageStatus.RECEIVED},
            PackageStatus.RECEIVED: {PackageStatus.IN_TRANSIT},
            PackageStatus.IN_TRANSIT: {PackageStatus.IN_TRANSIT, PackageStatus.OUT_FOR_DELIVERY},
            PackageStatus.OUT_FOR_DELIVERY: {PackageStatus.IN_TRANSIT, PackageStatus.DELIVERED},
            PackageStatus.DELIVERED: set(),
        }
        if event.status not in allowed_transitions[self.current_status]:
            raise ValueError(
                f"Cannot change status from '{self.current_status.value}' "
                f"to '{event.status.value}'."
            )
        self.events.append(event)
