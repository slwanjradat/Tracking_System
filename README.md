# Tracking System

A small Python package-tracking application focused on object-oriented programming and SQLite persistence.

## Run it

Requires Python 3.10 or newer. From the project folder, run:

```powershell
python -m tracking_system
```

Packages and their tracking histories are stored in `tracking_system.db` in the project folder. The database and tables are created automatically when the application starts.

## Features

- Create a package and receive a tracking number.
- Add tracking updates and view the event history.
- Reject invalid status transitions, such as moving a delivered package back into transit.
- Keep packages and tracking histories between program runs using SQLite.
- Continue generating tracking numbers from the existing database records.

## Database

The application stores package details in the `packages` table and each status update in the `tracking_events` table. Each tracking event is linked to its package by tracking number, allowing a package to have a complete event history.


## Status flow

`created -> received -> in_transit -> out_for_delivery -> delivered`

A package may pass through multiple `in_transit` events. An `out_for_delivery` package can return to `in_transit` if delivery fails.
