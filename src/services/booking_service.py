from datetime import timedelta

from flask import current_app

from src.extensions import db
from src.models import Booking, Notification, Resource

# Services layer: application use cases and business rules.


ACTIVE_BOOKING_STATUSES = ("PendingApproval", "Confirmed")


class BookingService:
    @staticmethod
    def check_resource_conflict(resource_id, candidate_start, candidate_end, exclude_booking_id=None):
        query = Booking.query.filter(
            Booking.resourceId == resource_id,
            Booking.status.in_(ACTIVE_BOOKING_STATUSES),
            candidate_start < Booking.endTime,
            candidate_end > Booking.startTime,
        )
        if exclude_booking_id:
            query = query.filter(Booking.bookingId != exclude_booking_id)
        return query.first() is not None

    @staticmethod
    def create_booking(user_id, resource_id, start_time, end_time, purpose, attendees_count):
        BookingService._validate_policy(resource_id, start_time, end_time)
        resource = Resource.query.get_or_404(resource_id)
        if resource.status in ("Maintenance", "Faulty"):
            raise ValueError("Resource is not eligible for booking")
        status = "PendingApproval" if resource.status == "Restricted" else "Confirmed"
        booking = Booking(
            userId=user_id,
            resourceId=resource_id,
            startTime=start_time,
            endTime=end_time,
            purpose=purpose,
            attendeesCount=attendees_count,
            status=status,
        )
        db.session.add(booking)
        db.session.flush()
        db.session.add(Notification(
            userId=user_id,
            relatedBookingId=booking.bookingId,
            type="Confirmation" if status == "Confirmed" else "ApprovalPending",
            message="Your booking has been confirmed." if status == "Confirmed" else "Your booking is pending approval.",
            status="Sent",
        ))
        db.session.commit()
        return booking

    @staticmethod
    def modify_booking(booking_id, user_id, start_time, end_time, purpose, attendees_count):
        booking = Booking.query.filter_by(bookingId=booking_id, userId=user_id).first_or_404()
        BookingService._validate_policy(
            booking.resourceId,
            start_time,
            end_time,
            exclude_booking_id=booking.bookingId,
        )
        booking.startTime = start_time
        booking.endTime = end_time
        booking.purpose = purpose
        booking.attendeesCount = attendees_count
        db.session.commit()
        return booking

    @staticmethod
    def cancel_booking(booking_id, user_id):
        booking = Booking.query.filter_by(bookingId=booking_id, userId=user_id).first_or_404()
        booking.status = "Cancelled"
        db.session.commit()
        return booking

    @staticmethod
    def list_user_bookings(user_id):
        return Booking.query.filter_by(userId=user_id).order_by(Booking.startTime.desc()).all()

    @staticmethod
    def list_pending_bookings():
        return Booking.query.filter_by(status="PendingApproval").order_by(Booking.startTime.asc()).all()

    @staticmethod
    def approve_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if booking.status != "PendingApproval":
            raise ValueError("Only pending bookings can be approved")
        if BookingService.check_resource_conflict(booking.resourceId, booking.startTime, booking.endTime, booking.bookingId):
            raise ValueError("Cannot approve because the slot now conflicts")
        booking.status = "Confirmed"
        db.session.commit()
        return booking

    @staticmethod
    def reject_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if booking.status != "PendingApproval":
            raise ValueError("Only pending bookings can be rejected")
        booking.status = "Rejected"
        db.session.commit()
        return booking

    @staticmethod
    def _validate_policy(resource_id, start_time, end_time, exclude_booking_id=None):
        if end_time <= start_time:
            raise ValueError("End time must be after start time")
        max_hours = current_app.config.get("MAX_BOOKING_HOURS", 4)
        if end_time - start_time > timedelta(hours=max_hours):
            raise ValueError(f"Booking duration cannot exceed {max_hours} hours")
        if BookingService.check_resource_conflict(resource_id, start_time, end_time, exclude_booking_id):
            raise ValueError("Selected timeslot conflicts with an existing booking")
