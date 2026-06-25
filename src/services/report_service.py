from src.extensions import db
from src.models import Booking, Department, Resource, User

# Services layer: application use cases and business rules.


class ReportService:
    @staticmethod
    def bookings_per_resource():
        rows = (
            db.session.query(Resource.name, db.func.count(Booking.bookingId))
            .join(Booking, Booking.resourceId == Resource.resourceId)
            .filter(Booking.status == "Confirmed")
            .group_by(Resource.resourceId, Resource.name)
            .order_by(Resource.name)
            .all()
        )
        return [{"resource_name": name, "booking_count": count} for name, count in rows]

    @staticmethod
    def bookings_per_department():
        rows = (
            db.session.query(Department.name, db.func.count(Booking.bookingId))
            .join(User, User.departmentId == Department.departmentId)
            .join(Booking, Booking.userId == User.userId)
            .filter(Booking.status == "Confirmed")
            .group_by(Department.departmentId, Department.name)
            .order_by(Department.name)
            .all()
        )
        return [{"department_name": name, "booking_count": count} for name, count in rows]

    @staticmethod
    def pending_approvals_count():
        return Booking.query.filter_by(status="PendingApproval").count()
