from datetime import datetime
from types import SimpleNamespace

from src.extensions import db
from src.models import Booking, Department, Resource, ResourceType

# Services layer: application use cases and business rules.


ACTIVE_BOOKING_STATUSES = ("PendingApproval", "Confirmed")


class ResourceService:
    @staticmethod
    def list_resource_types():
        return ResourceType.query.order_by(ResourceType.name).all()

    @staticmethod
    def list_departments():
        return Department.query.order_by(Department.name).all()

    @staticmethod
    def list_resources():
        return Resource.query.order_by(Resource.name).all()

    @staticmethod
    def get_resource(resource_id):
        return Resource.query.get_or_404(resource_id)

    @staticmethod
    def create_resource(name, location, capacity, features, status, department_id, resource_type_id):
        resource = Resource(
            name=name,
            location=location,
            capacity=capacity,
            features=features,
            status=status,
            departmentId=department_id,
            resourceTypeId=resource_type_id,
        )
        db.session.add(resource)
        db.session.commit()
        return resource

    @staticmethod
    def update_resource(resource_id, name, location, capacity, features, status, department_id, resource_type_id):
        resource = ResourceService.get_resource(resource_id)
        resource.name = name
        resource.location = location
        resource.capacity = capacity
        resource.features = features
        resource.status = status
        resource.departmentId = department_id
        resource.resourceTypeId = resource_type_id
        db.session.commit()
        return resource

    @staticmethod
    def update_resource_status(resource_id, status):
        resource = ResourceService.get_resource(resource_id)
        resource.status = status
        db.session.commit()
        return resource

    @staticmethod
    def search_available_resources(resource_type_id, location, date, start_time, end_time, capacity):
        query = Resource.query.filter(~Resource.status.in_(("Maintenance", "Faulty")))

        if resource_type_id:
            query = query.filter(Resource.resourceTypeId == int(resource_type_id))
        if location:
            query = query.filter(Resource.location.ilike(f"%{location}%"))
        if capacity:
            query = query.filter(Resource.capacity >= int(capacity))

        resources = query.order_by(Resource.name).all()
        if not (date and start_time and end_time):
            return [
                SimpleNamespace(resource=resource, is_available=True, availability_label="Select time", requires_approval=resource.status == "Restricted")
                for resource in resources
            ]

        candidate_start = datetime.fromisoformat(f"{date}T{start_time}")
        candidate_end = datetime.fromisoformat(f"{date}T{end_time}")
        results = []
        for resource in resources:
            has_conflict = Booking.query.filter(
                Booking.resourceId == resource.resourceId,
                Booking.status.in_(ACTIVE_BOOKING_STATUSES),
                candidate_start < Booking.endTime,
                candidate_end > Booking.startTime,
            ).first() is not None
            requires_approval = resource.status == "Restricted"
            label = "Busy" if has_conflict else ("Requires Approval" if requires_approval else "Free")
            results.append(SimpleNamespace(
                resource=resource,
                is_available=not has_conflict,
                availability_label=label,
                requires_approval=requires_approval,
            ))
        return results
