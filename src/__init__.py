from flask import Flask

from config import Config
from src.extensions import db
from src.models import Role
from src.routes import register_routes


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    db.init_app(app)
    register_routes(app)

    with app.app_context():
        db.create_all()
        seed_roles()

    return app


def seed_roles():
    roles = [
        ("Student", "Student user"),
        ("FacultyStaff", "Faculty or staff booker"),
        ("ResourceManager", "Resource manager"),
        ("Admin", "System administrator"),
    ]
    for name, description in roles:
        if not Role.query.filter_by(roleName=name).first():
            db.session.add(Role(roleName=name, description=description))
    db.session.commit()
