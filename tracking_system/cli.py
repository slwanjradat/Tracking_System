"""Command-line interface for the tracking system."""

from tracking_system.models import PackageStatus
from tracking_system.service import TrackingService

CREATE_PACKAGE = "1"
ADD_TRACKING_UPDATE = "2"
VIEW_PACKAGE_HISTORY = "3"
QUIT = "4"

STATUS_OPTIONS = {
    "1": PackageStatus.RECEIVED,
    "2": PackageStatus.IN_TRANSIT,
    "3": PackageStatus.OUT_FOR_DELIVERY,
    "4": PackageStatus.DELIVERED,
}


def show_package_info(package) -> None:
    print(f"\nPackage {package.tracking_number} for {package.recipient}")
    print(f"Current status: {package.current_status.value.replace('_', ' ')}")
    print("Tracking history:")
    for event in package.events:
        time = event.timestamp.astimezone().strftime("%Y-%m-%d %H:%M")
        print(f"  {time} | {event.status.value.replace('_', ' ')} | {event.location}")
        if event.note:
            print(f"    {event.note}")


def main() -> None:
    service = TrackingService()
    while True:
        print("\nPackage Tracking")
        print("1. Create a package")
        print("2. Add a tracking update")
        print("3. View package history")
        print("4. Quit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == CREATE_PACKAGE:
                package = service.create_package(input("Recipient name: "))
                print(f"Package created. Tracking number: {package.tracking_number}")
            elif choice == ADD_TRACKING_UPDATE:
                tracking_number = input("Tracking number: ").strip()
                print("Status: 1=received, 2=in transit, 3=out for delivery, 4=delivered")
                status = STATUS_OPTIONS.get(input("Choose status: ").strip())
                if status is None:
                    print("Unknown status option.")
                    continue
                location = input("Location: ")
                note = input("Note (optional): ")
                package = service.add_tracking_event(tracking_number, status, location, note)
                print(f"Updated. Current status: {package.current_status.value.replace('_', ' ')}")
            elif choice == VIEW_PACKAGE_HISTORY:
                package = service.get_package(input("Tracking number: ").strip())
                show_package_info(package)
            elif choice == QUIT:
                print("Goodbye!")
                break
            else:
                print("Please choose 1, 2, 3 or 4.")
        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
