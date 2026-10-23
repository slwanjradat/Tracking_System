"""Application service for package tracking."""

from datetime import datetime

from tracking_system.db_storage import (
    create_tables, get_next_tracking_number, load_packages,
    load_tracking_events, save_package, save_tracking_event,
)
from tracking_system.models import Package, PackageStatus, TrackingEvent

class TrackingService:
    """Creates packages and records their tracking events."""

    def __init__(self) -> None:
        create_tables()
        self._packages: dict[str, Package] = {}
        self._next_tracking_number = get_next_tracking_number()
        self._load_saved_packages()

    def _load_saved_packages(self) -> None:
        for row in load_packages():
            package = Package(
                tracking_number=row["tracking_number"],
                recipient=row["recipient"],
            )
            for event_row in load_tracking_events(package.tracking_number):
                package.events.append(
                    TrackingEvent(
                        status=PackageStatus(event_row["status"]),
                        location=event_row["location"],
                        note=event_row["note"],
                        timestamp=datetime.fromisoformat(event_row["timestamp"]),
                    )
                )
            self._packages[package.tracking_number] = package

    def create_package(self, recipient: str) -> Package:

        if not recipient.strip():
            raise ValueError("Recipient name cannot be empty.")
        
        ''' give the package a tracking number. for now it is a simple incrementing number, but in a real system it would be more complex. '''
        tracking_number = f"PKG-{self._next_tracking_number:03d}"
        self._next_tracking_number += 1
        
        package = Package(tracking_number=tracking_number, recipient=recipient.strip())
        initial_event = TrackingEvent(
            status=PackageStatus.CREATED,
            location="Sender",
            note="Shipping label created.",
        )
        save_package(package.tracking_number, package.recipient)
        save_tracking_event(
            package.tracking_number,
            initial_event.status.value,
            initial_event.location,
            initial_event.note,
            initial_event.timestamp.isoformat(),
        )
        package.events.append(initial_event)
        self._packages[tracking_number] = package
        return package

    def get_package(self, tracking_number: str) -> Package:
        try:
            return self._packages[tracking_number.upper()]
        except KeyError as error:
            raise KeyError(f"No package found with tracking number {tracking_number}.") from error

    def add_tracking_event(
        self,
        tracking_number: str,
        status: PackageStatus,
        location: str,
        note: str = "",
    ) -> Package:
        if not location.strip():
            raise ValueError("Location cannot be empty.")
        package = self.get_package(tracking_number)
        event = TrackingEvent(status=status, location=location.strip(), note=note.strip())
        package.add_event(event)
        save_tracking_event(
            package.tracking_number,
            event.status.value,
            event.location,
            event.note,
            event.timestamp.isoformat(),
        )
        return package
