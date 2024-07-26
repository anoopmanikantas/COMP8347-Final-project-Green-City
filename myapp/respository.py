import django
from .models import BuildingPermit
from django.db.models import Q


class Repository:
    def __init__(self, user_id: int = 0):
        self.user_id = user_id

    def get_building_permits(
            self,
            query: str = "",
    ) -> list:
        """
        Used to fetch building permits from the db
        :returns: Number of building permits
        """
        query_parameters = ['name', 'date', 'application_number', 'application_status']
        building_permits_count = 0

        for query_parameter in query_parameters:
            query_util = Q(**{f'{query_parameter}__icontains': query, 'user_id': self.user_id})
            results = BuildingPermit.objects.filter(query_util)
            if results.count() != 0:
                return results
            building_permits_count = results.count()

        if building_permits_count == 0:
            return []

    def get_all_building_permits(self) -> list:
        return BuildingPermit.objects.filter(user_id=self.user_id)

    def get_count_of_building_permits(self):
        submitted_applications = BuildingPermit.objects.filter(
            user_id=self.user_id
        ).count()
        pending_applications = BuildingPermit.objects.filter(
            application_status='in progress',
            user_id=self.user_id
        ).count()
        approved_applications = BuildingPermit.objects.filter(
            application_status='approved',
            user_id=self.user_id
        ).count()
        return submitted_applications, pending_applications, approved_applications

    class ApplicationDetails:
        def __init__(self, user_id):
            self.submitted = 0
            self.pending = 0
            self.approved = 0
            self.rejected = 0
            self.user_id = user_id
            self._populate_data()

        def _populate_data(self):
            repository = Repository(user_id=self.user_id)
            self.submitted, self.pending, self.approved = repository.get_count_of_building_permits()

    def get_application_details(self) -> ApplicationDetails:
        return self.ApplicationDetails(self.user_id)
