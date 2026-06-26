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
- Student/Faculty dashboard and My Bookings page.
- Edit or cancel eligible future bookings more than 24 hours before start time.
- Role-specific dashboards and navigation menus for bookers, managers, and admins.
- Resource Manager approval workflow.
- Resource Manager resource/status management.
- Admin reports.
- Admin user management.
- Vercel deployment entrypoint and routing configuration.
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

## Vercel Deployment

The project includes a minimal Vercel wrapper without changing the local Flask structure:

- `api/app.py` imports the existing `create_app()` factory and exposes a top-level `app`.
- `vercel.json` routes all requests to `api/app.py` using the Python runtime.

For deployment, push the repository to GitHub and import it in Vercel. Local development still uses `python app.py`.

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
| `/bookings/<booking_id>/edit` | Edit an eligible future booking |
| `/bookings/<booking_id>/cancel` | Cancel an eligible future booking |
| `/bookings/pending` | Manager/Admin approval workflow |
| `/manager/resources` | Manager/Admin resource management |
| `/admin/report` | Admin reporting |
| `/admin/users` | Admin user management |

## Role-Based Navigation

After login, the top navigation changes by role:

| Role | Menu |
|---|---|
| Student / FacultyStaff | Home, Search, My Bookings, Dashboard, Profile, Logout |
| ResourceManager | Home, Dashboard, Resources, Approvals, Profile, Logout |
| Admin | Home, Dashboard, Resources, Approvals, Users, Report, Profile, Logout |

Managers and admins do not see end-user booking links such as Search or My Bookings. Those routes are also protected by role-based access control.

## Project Structure

```text
booksystem/
  app.py
  api/
    app.py
  config.py
  requirements.txt
  vercel.json
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
- Notification delivery is stubbed as database rows; no email/SMS delivery is implemented.
- Recurrence and maintenance records exist as models, but recurring booking and maintenance scheduling UI are not implemented.
- SQLite is suitable for the prototype. For persistent production deployment on serverless platforms, configure an external database with `DATABASE_URL`.

