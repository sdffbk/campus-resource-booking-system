from src.extensions import db

# Models layer: SQLAlchemy entities for the SDS data dictionary.


class Role(db.Model):
    roleId = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))


class Department(db.Model):
    departmentId = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)


class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    universityId = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(40))
    accountStatus = db.Column(db.String(30), nullable=False, default="Active")
    createdAt = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    lastLoginAt = db.Column(db.DateTime)
    roleId = db.Column(db.Integer, db.ForeignKey("role.roleId"), nullable=False)
    departmentId = db.Column(db.Integer, db.ForeignKey("department.departmentId"), nullable=False)

    role = db.relationship("Role")
    department = db.relationship("Department")


class ResourceType(db.Model):
    resourceTypeId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class Resource(db.Model):
    resourceId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False, default="Available")
    departmentId = db.Column(db.Integer, db.ForeignKey("department.departmentId"), nullable=False)
    resourceTypeId = db.Column(db.Integer, db.ForeignKey("resource_type.resourceTypeId"), nullable=False)

    department = db.relationship("Department")
    resourceType = db.relationship("ResourceType")


class RecurrencePattern(db.Model):
    recurrencePatternId = db.Column(db.Integer, primary_key=True)
    patternType = db.Column(db.String(40))
    dayOfWeek = db.Column(db.String(20))
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)


class Booking(db.Model):
    bookingId = db.Column(db.Integer, primary_key=True)
    resourceId = db.Column(db.Integer, db.ForeignKey("resource.resourceId"), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    attendeesCount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Confirmed")
    createdAt = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    recurrencePatternId = db.Column(db.Integer, db.ForeignKey("recurrence_pattern.recurrencePatternId"))

    resource = db.relationship("Resource")
    user = db.relationship("User")
    recurrencePattern = db.relationship("RecurrencePattern")


class MaintenanceRecord(db.Model):
    maintenanceId = db.Column(db.Integer, primary_key=True)
    resourceId = db.Column(db.Integer, db.ForeignKey("resource.resourceId"), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(30), nullable=False, default="Scheduled")


class Notification(db.Model):
    notificationId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable=False)
    relatedBookingId = db.Column(db.Integer, db.ForeignKey("booking.bookingId"))
    relatedMaintenanceId = db.Column(db.Integer, db.ForeignKey("maintenance_record.maintenanceId"))
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    sentAt = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(30), nullable=False, default="Sent")
