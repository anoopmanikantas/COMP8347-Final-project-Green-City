import django
from .models import BuildingPermit
from django.db.models import Q


class Repository:
    def __init__(self):
        pass

    def get_building_permits(
            self,
            query: str = "",
            user_id: int = 0
    ) -> list:
        """
        Used to fetch building permits from the db
        :returns: Number of building permits
        """
        query_parameters = ['name', 'date', 'application_number', 'application_status']
        building_permits_count = 0

        for query_parameter in query_parameters:
            query_util = Q(**{f'{query_parameter}__icontains': query, 'user_id': user_id})
            results = BuildingPermit.objects.filter(query_util)
            if results.count() != 0:
                return results
            building_permits_count = results.count()

        if building_permits_count == 0:
            return BuildingPermit.objects.filter(user_id=user_id)
