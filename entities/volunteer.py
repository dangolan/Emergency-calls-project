from entities.geoPoint import GeoPoint


class Volunteer:
    def __init__(
        self,
        id,
        uniqueIdNumber,
        firstName,
        lastName,
        phone,
        city,
        street,
        houseNumber,
        imageUrl,
        latitude=None,
        longitude=None,
    ):
        self.id = id
        self.uniqueIdNumber = uniqueIdNumber
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.city = city
        self.street = street
        self.houseNumber = houseNumber
        self.imageUrl = imageUrl
        self.geoPoint = GeoPoint(latitude, longitude)
