# Platform Walkthrough Guide

This guide explains how to demonstrate the Campus Resource Booking System by role.

Start the system first:

```powershell
python seed_demo_data.py
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 1. Student / User Walkthrough

Login:

```text
student@example.com
Student123!
```

Student users can search resources, create bookings, and view their own bookings.

Student navigation shows:

```text
Home | Search | My Bookings | Dashboard | Profile | Logout
```

### Search and Book a Resource

1. Click `Search`.
2. Enter a date, start time, and end time.
3. Optionally filter by resource type, location, or capacity.
4. Review the availability column:
   - `Free`: booking can be submitted and becomes `Confirmed`.
   - `Requires Approval`: booking can be submitted and becomes `PendingApproval`.
   - `Busy`: booking button is disabled.
   - `Select time`: choose date/start/end time first.
5. Click `Book` or `Request Booking`.
6. Go to `My Bookings` to confirm the booking appears.

### Dashboard

1. Click `Dashboard`.
2. View upcoming bookings.
3. Confirm that both `Confirmed` and `PendingApproval` bookings are shown.

### My Bookings

1. Click `My Bookings`.
2. Review booking resource, date, time, and status.
3. Future bookings more than 24 hours away show working `Edit` and `Cancel` actions.
4. Click `Edit` to change date, time, purpose, or attendee count.
5. Click `Cancel` to mark the booking as `Cancelled`.

If the edited booking is for a `Restricted` resource, it returns to `PendingApproval` so a Resource Manager or Admin can approve the changed request again.

## 2. Resource Manager Walkthrough

Login:

```text
manager@example.com
Manager123!
```

Resource Managers can approve restricted bookings and manage resource availability/status.

Resource Manager navigation shows:

```text
Home | Dashboard | Resources | Approvals | Profile | Logout
```

The manager dashboard shows operational counts and management actions instead of personal upcoming bookings.

### Approvals

1. Click `Approvals`.
2. Review pending booking requests.
3. Click `Approve` to change status to `Confirmed`.
4. Click `Reject` to change status to `Rejected`.

This demonstrates the approval use case for restricted/specialized resources.

### Resource Management

1. Click `Resources`.
2. View all resources with type, location, capacity, and status.
3. Click `Edit` for a resource.
4. Change fields such as location, capacity, features, or status.
5. Set status to:
   - `Available`: resource can be searched/booked.
   - `Restricted`: booking requires approval.
   - `Maintenance` or `Faulty`: resource is excluded from search/booking.
6. Save changes.

### Add Resource

1. Go to `Resources`.
2. Click `Add Resource`.
3. Fill in resource name, type, department, location, capacity, features, and status.
4. Save.

## 3. Admin Walkthrough

Login:

```text
admin@example.com
Admin123!
```

Admins can access all manager features plus reports and user management.

Admin navigation shows:

```text
Home | Dashboard | Resources | Approvals | Users | Report | Profile | Logout
```

The admin dashboard shows system-wide counts and management actions instead of personal upcoming bookings.

### Report

1. Click `Report`.
2. Review:
   - Bookings per resource.
   - Bookings per department.
   - Pending approvals count.
3. Click `Export PDF`.
4. Use the browser print dialog to save the report as PDF.

### Users

1. Click `Users`.
2. Review user details:
   - Name
   - University ID
   - Email
   - Role
   - Department
   - Account status
3. Change account status:
   - `Active`
   - `PendingVerification`
   - `Locked`
4. Change user role:
   - `Student`
   - `FacultyStaff`
   - `ResourceManager`
   - `Admin`
5. Submit the change.

Safety checks prevent the current admin from disabling their own account or removing their own Admin role.

## 4. Role-Based Access Checks

Use these quick checks during the demo:

- Student can access:
  - Home
  - Search
  - Dashboard
  - My Bookings
- Student cannot access:
  - Approvals
  - Resource Management
  - Report
  - Users
- Resource Manager can access:
  - Approvals
  - Resource Management
- Resource Manager cannot access:
  - Search
  - My Bookings
  - Report
  - Users
- Admin can access:
  - Approvals
  - Resource Management
  - Report
  - Users
- Admin cannot access:
  - Search
  - My Bookings

## 5. SRS/SDS Alignment Talking Points

Use this mapping in your presentation:

| SRS/SDS Concept | Prototype Implementation |
|---|---|
| Student User | Registration, login, search, book, My Bookings, Dashboard |
| Faculty/Staff Booker | Supported as a role in user management |
| Resource Manager | Approvals and resource status management |
| System Administrator | Reports and user/role/status management |
| Resource Catalog | `Resource`, `ResourceType`, search page |
| Booking Management | `BookingService`, create/edit/cancel booking, conflict detection |
| Approval Workflow | Restricted resources create `PendingApproval` bookings |
| Maintenance Handling | Resource status `Maintenance`/`Faulty` excludes booking |
| Notification Stub | `Notification` rows are created on booking submission |
| Reporting | Admin report by resource and department |
| 3-Tier Architecture | Models, Services, Controllers/Routes/Templates |

## 6. Suggested Demo Flow

1. Login as Student.
2. Search for resources with date/time.
3. Book an available resource.
4. Request a restricted resource.
5. Show My Bookings, then edit or cancel an eligible future booking.
6. Show the Student Dashboard.
7. Logout.
8. Login as Resource Manager.
9. Review the Manager Dashboard.
10. Approve or reject pending booking.
11. Edit a resource status.
12. Logout.
13. Login as Admin.
14. Review the Admin Dashboard.
15. Show Report.
16. Show Users and role/status controls.

