from functools import wraps

from flask import flash, redirect, session

from src.controllers import auth_controller, booking_controller, page_controller

# Routes layer: URL mapping and access-control middleware.


def login_required(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect("/login")
        return handler(*args, **kwargs)
    return wrapper


def admin_required(handler):
    return role_required("Admin")(handler)


def approval_required(handler):
    return role_required("Admin", "ResourceManager")(handler)


def booker_required(handler):
    return role_required("Student", "FacultyStaff")(handler)


def role_required(*role_names):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")
            if session.get("role_name") not in role_names:
                flash("You are not authorized to access that page.", "danger")
                return redirect("/dashboard")
            return handler(*args, **kwargs)
        return wrapper
    return decorator


def register_routes(app):
    app.add_url_rule("/", view_func=page_controller.home, methods=["GET"])
    app.add_url_rule(
        "/dashboard",
        view_func=login_required(page_controller.dashboard),
        methods=["GET"],
    )
    app.add_url_rule("/register", view_func=auth_controller.register_form, methods=["GET"])
    app.add_url_rule("/register", view_func=auth_controller.register, methods=["POST"])
    app.add_url_rule("/login", view_func=auth_controller.login_form, methods=["GET"])
    app.add_url_rule("/login", view_func=auth_controller.login, methods=["POST"])
    app.add_url_rule("/logout", view_func=auth_controller.logout, methods=["POST"])
    app.add_url_rule(
        "/bookings",
        view_func=booker_required(booking_controller.create_booking),
        methods=["POST"],
    )
    app.add_url_rule(
        "/bookings/new/<int:resource_id>",
        view_func=booker_required(booking_controller.new_booking_form),
        methods=["GET"],
    )
    app.add_url_rule(
        "/resources/search",
        view_func=booker_required(page_controller.search_resources),
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/bookings/mine",
        view_func=booker_required(page_controller.my_bookings),
        methods=["GET"],
    )
    app.add_url_rule(
        "/profile",
        view_func=login_required(page_controller.profile),
        methods=["GET"],
    )
    app.add_url_rule(
        "/admin/report",
        view_func=admin_required(page_controller.admin_report),
        methods=["GET"],
    )
    app.add_url_rule(
        "/bookings/pending",
        view_func=approval_required(page_controller.pending_bookings),
        methods=["GET"],
    )
    app.add_url_rule(
        "/bookings/<int:booking_id>/approve",
        view_func=approval_required(booking_controller.approve_booking),
        methods=["POST"],
    )
    app.add_url_rule(
        "/bookings/<int:booking_id>/reject",
        view_func=approval_required(booking_controller.reject_booking),
        methods=["POST"],
    )
    app.add_url_rule(
        "/manager/resources",
        view_func=role_required("Admin", "ResourceManager")(page_controller.list_resources),
        methods=["GET"],
    )
    app.add_url_rule(
        "/manager/resources/new",
        view_func=role_required("Admin", "ResourceManager")(page_controller.create_resource),
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/manager/resources/<int:resource_id>/edit",
        view_func=role_required("Admin", "ResourceManager")(page_controller.edit_resource),
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/manager/resources/<int:resource_id>/status",
        view_func=role_required("Admin", "ResourceManager")(page_controller.set_resource_status),
        methods=["POST"],
    )
    app.add_url_rule(
        "/admin/users",
        view_func=admin_required(page_controller.list_users),
        methods=["GET"],
    )
    app.add_url_rule(
        "/admin/users/<int:user_id>/status",
        view_func=admin_required(page_controller.set_user_status),
        methods=["POST"],
    )
    app.add_url_rule(
        "/admin/users/<int:user_id>/role",
        view_func=admin_required(page_controller.set_user_role),
        methods=["POST"],
    )
