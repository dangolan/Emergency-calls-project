from entities.geoPoint import GeoPoint


class Event:
    def __init__(self, id, description, latitude, longitude, address, time, status):
        self.id = id
        self.description = description
        self.geoPoint = GeoPoint(latitude, longitude)
        self.address = address
        self.time = time
        self.status = status
