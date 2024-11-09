from entities.geoPoint import GeoPoint


class Volunteer:
    def __init__(
        self, id, firstName, lastName, phone, latitude, longitude, address, type, image
    ):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.geoPoint = GeoPoint(latitude, longitude)
        self.address = address
        self.phone = phone
        self.type = type
        self.image = image
