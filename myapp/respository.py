import django
from .models import BuildingPermit


class Repository:
    def __init__(self):
        pass

    def get_building_permits(self, name: str = "", application_number: str = "") -> list:
        """
        Used to fetch building permits from the db
        :returns: Number of building permits
        """
        if name != "":
            building_permits = BuildingPermit.objects.filter(name__icontains=name)
        elif application_number != "":
            building_permits = BuildingPermit.objects.filter(application_number__icontains=application_number)
        else:
            building_permits = BuildingPermit.objects.all()
        return building_permits



