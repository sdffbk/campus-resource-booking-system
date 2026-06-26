from datetime import datetime, timedelta

from flask import flash, redirect, render_template, request, session

from src.models import Booking, Resource, User
from src.services.booking_service import BookingService
from src.services.report_service import ReportService
from src.services.resource_service import ResourceService
from src.services.user_service import UserService

# Controllers layer: maps HTTP requests to service calls.


def home():
    return render_template("home.html")


def dashboard():
    role_name = session.get("role_name")
    if role_name in ("Admin", "ResourceManager"):
        dashboard_stats = {
            "pending_approvals": ReportService.pending_approvals_count(),
            "total_resources": Resource.query.count(),
            "unavailable_resources": Resource.query.filter(Resource.status.in_(("Maintenance", "Faulty"))).count(),
            "confirmed_bookings": Booking.query.filter_by(status="Confirmed").count(),
        }
        if role_name == "Admin":
            dashboard_stats["active_users"] = User.query.filter_by(accountStatus="Active").count()
        return render_template("dashboard.html", dashboard_stats=dashboard_stats)

    bookings = BookingService.list_user_bookings(session["user_id"])
    upcoming_bookings = [booking for booking in bookings if booking.startTime > datetime.utcnow()]
    return render_template("dashboard.html", upcoming_bookings=upcoming_bookings)


def search_resources():
    resource_types = ResourceService.list_resource_types()
    results = ResourceService.search_available_resources(None, None, None, None, None, None)
    form = request.form if request.method == "POST" else {}
    if request.method == "POST":
        results = ResourceService.search_available_resources(
            resource_type_id=form.get("resourceTypeId"),
            location=form.get("location"),
            date=form.get("date"),
            start_time=form.get("startTime"),
            end_time=form.get("endTime"),
            capacity=form.get("capacity"),
        )
    return render_template(
        "search_resources.html",
        resource_types=resource_types,
        results=results,
        form=form,
    )


def my_bookings():
    bookings = BookingService.list_user_bookings(session["user_id"])
    return render_template(
        "my_bookings.html",
        bookings=bookings,
        now=datetime.utcnow(),
        timedelta=timedelta,
    )


def profile():
    return render_template("profile.html", user=UserService.get_user(session["user_id"]))


def admin_report():
    if session.get("role_name") != "Admin":
        flash("You are not authorized to view the admin report.", "danger")
        return redirect("/dashboard" if session.get("user_id") else "/")
    return render_template(
        "admin_report.html",
        resource_rows=ReportService.bookings_per_resource(),
        department_rows=ReportService.bookings_per_department(),
        pending_approvals_count=ReportService.pending_approvals_count(),
    )


def pending_bookings():
    if session.get("role_name") not in ("Admin", "ResourceManager"):
        flash("You are not authorized to manage booking approvals.", "danger")
        return redirect("/dashboard")
    return render_template("pending_bookings.html", bookings=BookingService.list_pending_bookings())


def list_resources():
    return render_template("manager_resources.html", resources=ResourceService.list_resources())


def create_resource():
    if request.method == "POST":
        ResourceService.create_resource(
            name=request.form["name"],
            location=request.form["location"],
            capacity=int(request.form["capacity"]),
            features=request.form.get("features"),
            status=request.form["status"],
            department_id=int(request.form["departmentId"]),
            resource_type_id=int(request.form["resourceTypeId"]),
        )
        flash("Resource created.", "success")
        return redirect("/manager/resources")
    return render_template(
        "edit_resource.html",
        resource=None,
        resource_types=ResourceService.list_resource_types(),
        departments=ResourceService.list_departments(),
    )


def edit_resource(resource_id):
    resource = ResourceService.get_resource(resource_id)
    if request.method == "POST":
        ResourceService.update_resource(
            resource_id=resource_id,
            name=request.form["name"],
            location=request.form["location"],
            capacity=int(request.form["capacity"]),
            features=request.form.get("features"),
            status=request.form["status"],
            department_id=int(request.form["departmentId"]),
            resource_type_id=int(request.form["resourceTypeId"]),
        )
        flash("Resource updated.", "success")
        return redirect("/manager/resources")
    return render_template(
        "edit_resource.html",
        resource=resource,
        resource_types=ResourceService.list_resource_types(),
        departments=ResourceService.list_departments(),
    )


def set_resource_status(resource_id):
    ResourceService.update_resource_status(resource_id, request.form["status"])
    flash("Resource status updated.", "success")
    return redirect("/manager/resources")


def list_users():
    return render_template(
        "admin_users.html",
        users=UserService.list_users(),
        roles=UserService.list_roles(),
        statuses=["Active", "PendingVerification", "Locked"],
    )


def set_user_status(user_id):
    try:
        UserService.set_user_status(user_id, request.form["accountStatus"], session["user_id"])
        flash("User status updated.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect("/admin/users")


def set_user_role(user_id):
    try:
        UserService.set_user_role(user_id, request.form["roleName"], session["user_id"])
        flash("User role updated.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect("/admin/users")
