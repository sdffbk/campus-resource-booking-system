from datetime import datetime

import bcrypt

from src.extensions import db
from src.models import Department, Role, User

# Services layer: application use cases and business rules.


class AuthService:
    @staticmethod
    def register(name, university_id, email, password, department):
        email = email.lower()
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        if User.query.filter_by(universityId=university_id).first():
            raise ValueError("University ID already registered")

        role = Role.query.filter_by(roleName="Student").first()
        if not role:
            role = Role(roleName="Student", description="Student user")
            db.session.add(role)
            db.session.flush()
        dept = Department.query.filter(
            (Department.code == department) | (Department.name == department)
        ).first()
        if not dept:
            dept = Department(code=department.upper().replace(" ", "_"), name=department)
            db.session.add(dept)
            db.session.flush()

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            name=name,
            universityId=university_id,
            email=email,
            passwordHash=password_hash,
            roleId=role.roleId,
            departmentId=dept.departmentId,
            accountStatus="Active",
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email.lower()).first()
        if not user or user.accountStatus != "Active":
            raise ValueError("Invalid email or password")
        if not bcrypt.checkpw(password.encode("utf-8"), user.passwordHash.encode("utf-8")):
            raise ValueError("Invalid email or password")

        user.lastLoginAt = datetime.utcnow()
        db.session.commit()
        return user
