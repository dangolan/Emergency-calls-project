from entities.geoPoint import GeoPoint


class Volunteer:
    def __init__(
        self, id,uniqueIdNumber, firstName, lastName, phone, latitude, longitude,city,street,houseNumber, imageUrl):
        self.id = id
        self.uniqueIdNumber = uniqueIdNumber
        self.firstName = firstName
        self.lastName = lastName
        self.geoPoint = GeoPoint(latitude, longitude)
        self.phone = phone
        self.city = city
        self.street = street
        self.houseNumber = houseNumber
        self.imageUrl = imageUrl