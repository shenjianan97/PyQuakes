class _Address:
    """
    Private class for representing addresses. Not part of the API.
    """
    def __init__(self):
        self.address_line = None
        self.admin_district = None
        self.admin_district2 = None
        self.country_region = None
        self.country_region_iso2 = None
        self.formatted_address = None
        self.locality = None
        self.postal_code = None

    def set_address_line(self, address_line) -> '_Address':
        self.address_line = address_line
        return self

    def set_admin_district(self, admin_district) -> '_Address':
        self.admin_district = admin_district
        return self

    def set_admin_district2(self, admin_district2) -> '_Address':
        self.admin_district2 = admin_district2
        return self

    def set_country_region(self, country_region) -> '_Address':
        self.country_region = country_region
        return self

    def set_country_region_iso2(self, country_region_iso2) -> '_Address':
        self.country_region_iso2 = country_region_iso2
        return self

    def set_formatted_address(self, formatted_address) -> '_Address':
        self.formatted_address = formatted_address
        return self

    def set_locality(self, locality) -> '_Address':
        self.locality = locality
        return self

    def set_postal_code(self, postal_code) -> '_Address':
        self.postal_code = postal_code
        return self

    def get_address_line(self):
        return self.address_line

    def get_admin_district(self):
        return self.admin_district

    def get_admin_district2(self):
        return self.admin_district2

    def get_country_region(self):
        return self.country_region

    def get_formatted_address(self):
        return self.formatted_address

    def get_locality(self):
        return self.locality

    def get_postal_code(self):
        return self.postal_code

    def get_value(self):
        return self.__dict__