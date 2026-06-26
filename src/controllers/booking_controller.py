from datetime import datetime

from flask import flash, redirect, render_template, request, session

from src.services.booking_service import BookingService
from src.services.resource_service import ResourceService

# Controllers layer: maps HTTP requests to service calls.


def new_booking_form(resource_id):
    date = request.args.get("date")
    start_time = request.args.get("startTime")
    end_time = request.args.get("endTime")
    if not date or not start_time or not end_time:
        flash("Please select a date, start time, and end time before booking.", "warning")
        return redirect("/resources/search")
    return render_template(
        "create_booking.html",
        resource=ResourceService.get_resource(resource_id),
        date=date,
        start_time=start_time,
        end_time=end_time,
    )


def create_booking():
    date = request.form.get("date")
    if not date or not request.form.get("startTime") or not request.form.get("endTime"):
        flash("Please select a date, start time, and end time before booking.", "warning")
        return redirect("/resources/search")
    start_time = datetime.fromisoformat(f"{date}T{request.form['startTime']}")
    end_time = datetime.fromisoformat(f"{date}T{request.form['endTime']}")
    try:
        BookingService.create_booking(
            user_id=session["user_id"],
            resource_id=int(request.form["resourceId"]),
            start_time=start_time,
            end_time=end_time,
            purpose=request.form["purpose"],
            attendees_count=int(request.form["attendeesCount"]),
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect("/resources/search")
    flash("Booking submitted successfully.", "success")
    return redirect("/bookings/mine")


def edit_booking_form(booking_id):
    booking = BookingService.get_user_booking(booking_id, session["user_id"])
    if not BookingService.can_user_change_booking(booking):
        flash("This booking can no longer be edited.", "warning")
        return redirect("/bookings/mine")
    return render_template("edit_booking.html", booking=booking)


def edit_booking(booking_id):
    booking = BookingService.get_user_booking(booking_id, session["user_id"])
    if not BookingService.can_user_change_booking(booking):
        flash("This booking can no longer be edited.", "warning")
        return redirect("/bookings/mine")

    date = request.form.get("date")
    if not date or not request.form.get("startTime") or not request.form.get("endTime"):
        flash("Please select a date, start time, and end time.", "warning")
        return redirect(f"/bookings/{booking_id}/edit")

    start_time = datetime.fromisoformat(f"{date}T{request.form['startTime']}")
    end_time = datetime.fromisoformat(f"{date}T{request.form['endTime']}")
    try:
        BookingService.modify_booking(
            booking_id=booking_id,
            user_id=session["user_id"],
            start_time=start_time,
            end_time=end_time,
            purpose=request.form["purpose"],
            attendees_count=int(request.form["attendeesCount"]),
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect(f"/bookings/{booking_id}/edit")

    flash("Booking updated.", "success")
    return redirect("/bookings/mine")


def cancel_booking(booking_id):
    booking = BookingService.get_user_booking(booking_id, session["user_id"])
    if not BookingService.can_user_change_booking(booking):
        flash("This booking can no longer be cancelled.", "warning")
        return redirect("/bookings/mine")
    BookingService.cancel_booking(booking_id, session["user_id"])
    flash("Booking cancelled.", "success")
    return redirect("/bookings/mine")


def approve_booking(booking_id):
    try:
        BookingService.approve_booking(booking_id)
        flash("Booking approved.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect("/bookings/pending")


def reject_booking(booking_id):
    try:
        BookingService.reject_booking(booking_id)
        flash("Booking rejected.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect("/bookings/pending")
