# Campus Resource Booking System

Prototype web application for the CSE6214 Campus Resource Booking System project.

The system supports the main actors described in the SRS/SDS:

- Student / Faculty-Staff Booker
- Resource Manager
- System Administrator

It uses a simple 3-tier Flask architecture:

- Models/data layer: `src/models/`
- Services/business logic layer: `src/services/`
- Controllers/routes/presentation layer: `src/controllers/` and `src/routes/`
- Templates/UI: `src/templates/`

## Features

- Register and login with session-based authentication.
- Role-based navigation and access control.
- Search resources by type, location, date/time, and capacity.
- Check availability against existing bookings.
- Create bookings:
  - Available resources are auto-confirmed.
  - Restricted resources create `PendingApproval` bookings.
  - Busy/conflicting slots are blocked.
- Student dashboard and My Bookings page.
- Resource Manager approval workflow.
- Resource Manager resource/status management.
- Admin reports.
- Admin user management.
- Demo seed data for presentation/testing.

## Technology Stack

- Python 3.14
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- SQLite for prototype database
- Bootstrap 5 via CDN

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

If your terminal does not recognize `python`, set the alias:

```powershell
Set-Alias python "C:\Users\amahm\AppData\Local\Python\pythoncore-3.14-64\python.exe"
```

Seed demo data:

```powershell
python seed_demo_data.py
```

Run the application:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demo Accounts

After running `seed_demo_data.py`, use these accounts:

| Role | Email | Password |
|---|---|---|
| Student | `student@example.com` | `Student123!` |
| Resource Manager | `manager@example.com` | `Manager123!` |
| Admin | `admin@example.com` | `Admin123!` |

## Main Routes

| Route | Purpose |
|---|---|
| `/` | Home page |
| `/register` | Register student account |
| `/login` | Login |
| `/dashboard` | User dashboard |
| `/resources/search` | Search and book resources |
| `/bookings/mine` | View current user's bookings |
| `/bookings/pending` | Manager/Admin approval workflow |
| `/manager/resources` | Manager/Admin resource management |
| `/admin/report` | Admin reporting |
| `/admin/users` | Admin user management |

## Project Structure

```text
booksystem/
  app.py
  config.py
  requirements.txt
  seed_demo_data.py
  src/
    __init__.py
    extensions.py
    models/
    services/
    controllers/
    routes/
    templates/
```

## Notes

This is a university prototype, so some production features are simplified:

- Email verification is skipped.
- Availability uses bookings and resource status rather than a separate timeslot table.
- PDF export uses the browser print dialog.
- Edit/cancel booking UI is present, with full edit/cancel behavior kept minimal.

