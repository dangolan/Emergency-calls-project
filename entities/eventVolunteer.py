from entities.volunteer import Volunteer
class EventVolunteer:
    def __init__(self, volunteer : Volunteer, distance, duration, routeCoordinates):
        self.volunteer = volunteer  # An instance of Volunteer class
        self.distance = distance
        self.duration = duration
        self.routeCoordinates = routeCoordinates  # List of coordinate pairs
