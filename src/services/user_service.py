from src.extensions import db
from src.models import Role, User

# Services layer: application use cases and business rules.


class UserService:
    @staticmethod
    def get_user(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def list_users():
        return User.query.order_by(User.name).all()

    @staticmethod
    def list_roles():
        return Role.query.order_by(Role.roleName).all()

    @staticmethod
    def set_user_status(user_id, new_status, current_user_id):
        if user_id == current_user_id and new_status != "Active":
            raise ValueError("You cannot disable your own account.")
        user = User.query.get_or_404(user_id)
        user.accountStatus = new_status
        db.session.commit()
        return user

    @staticmethod
    def set_user_role(user_id, role_name, current_user_id):
        if user_id == current_user_id and role_name != "Admin":
            raise ValueError("You cannot remove your own Admin role.")
        role = Role.query.filter_by(roleName=role_name).first()
        if not role:
            raise ValueError("Invalid role.")
        user = User.query.get_or_404(user_id)
        user.roleId = role.roleId
        db.session.commit()
        return user
