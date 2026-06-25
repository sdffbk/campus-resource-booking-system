from datetime import datetime, timedelta

import bcrypt

from src import create_app
from src.extensions import db
from src.models import Booking, Department, Resource, ResourceType, Role, User


def get_or_create(model, defaults=None, **filters):
    item = model.query.filter_by(**filters).first()
    if item:
        return item
    item = model(**filters, **(defaults or {}))
    db.session.add(item)
    db.session.flush()
    return item


def password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def get_or_create_user(name, university_id, email, password, role_name, department):
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    role = Role.query.filter_by(roleName=role_name).first()
    user = User(
        name=name,
        universityId=university_id,
        email=email,
        passwordHash=password_hash(password),
        accountStatus="Active",
        roleId=role.roleId,
        departmentId=department.departmentId,
    )
    db.session.add(user)
    db.session.flush()
    return user


def get_or_create_booking(resource, user, start_time, end_time, purpose, attendees_count, status):
    booking = Booking.query.filter_by(resourceId=resource.resourceId, userId=user.userId, startTime=start_time).first()
    if booking:
        return booking
    booking = Booking(
        resourceId=resource.resourceId,
        userId=user.userId,
        startTime=start_time,
        endTime=end_time,
        purpose=purpose,
        attendeesCount=attendees_count,
        status=status,
    )
    db.session.add(booking)
    db.session.flush()
    return booking


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        roles = {
            "Student": "Student user",
            "FacultyStaff": "Faculty or staff booker",
            "ResourceManager": "Resource manager",
            "Admin": "System administrator",
        }
        for name, description in roles.items():
            get_or_create(Role, roleName=name, defaults={"description": description})

        fci = get_or_create(Department, code="FCI", defaults={"name": "Faculty of Computing and Informatics"})
        fom = get_or_create(Department, code="FOM", defaults={"name": "Faculty of Management"})

        meeting_room = get_or_create(ResourceType, name="MeetingRoom", defaults={"description": "Meeting room"})
        lab = get_or_create(ResourceType, name="Lab", defaults={"description": "Computer lab"})
        projector = get_or_create(ResourceType, name="Projector", defaults={"description": "Portable projector"})

        admin = get_or_create_user("Demo Admin", "ADMIN001", "admin@example.com", "Admin123!", "Admin", fci)
        student = get_or_create_user("Demo Student", "STU001", "student@example.com", "Student123!", "Student", fci)
        manager = get_or_create_user("Demo Manager", "MGR001", "manager@example.com", "Manager123!", "ResourceManager", fom)

        resources = [
            ("Discussion Room A", "Library Level 2", 8, "Whiteboard, screen", "Available", fci, meeting_room),
            ("Seminar Room B", "Block C", 30, "Projector, microphones", "Available", fom, meeting_room),
            ("AI Lab 1", "FCI Lab Wing", 40, "PCs, GPU workstation", "Available", fci, lab),
            ("Restricted Research Lab", "FCI Secure Wing", 12, "Specialized equipment", "Restricted", fci, lab),
            ("Mobile Projector 01", "Equipment Counter", 1, "HDMI, VGA", "Available", fci, projector),
            ("Maintenance Room", "Block D", 20, "Under servicing", "Maintenance", fom, meeting_room),
        ]
        created_resources = {}
        for name, location, capacity, features, status, department, resource_type in resources:
            resource = get_or_create(
                Resource,
                name=name,
                defaults={
                    "location": location,
                    "capacity": capacity,
                    "features": features,
                    "status": status,
                    "departmentId": department.departmentId,
                    "resourceTypeId": resource_type.resourceTypeId,
                },
            )
            created_resources[name] = resource

        demo_day = datetime(2026, 7, 1)
        get_or_create_booking(created_resources["Discussion Room A"], student, demo_day.replace(hour=10), demo_day.replace(hour=12), "Group discussion", 6, "Confirmed")
        get_or_create_booking(created_resources["Seminar Room B"], manager, demo_day.replace(hour=14), demo_day.replace(hour=16), "Faculty briefing", 20, "Confirmed")
        get_or_create_booking(created_resources["Restricted Research Lab"], student, demo_day.replace(hour=9), demo_day.replace(hour=11), "Prototype testing", 4, "PendingApproval")
        get_or_create_booking(created_resources["AI Lab 1"], admin, demo_day + timedelta(days=2, hours=1), demo_day + timedelta(days=2, hours=3), "Admin workshop", 15, "Confirmed")

        db.session.commit()
        print("Demo data seeded.")
        print("Admin: admin@example.com / Admin123!")
        print("Student: student@example.com / Student123!")
        print("Resource Manager: manager@example.com / Manager123!")


if __name__ == "__main__":
    seed()
