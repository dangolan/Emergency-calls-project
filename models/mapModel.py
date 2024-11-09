import io
import random
import folium
import requests


class mapModel:
    def __init__(self):
        pass

    def get_volunteers_route(self, eventLat, eventLon):
        volunteersRoute = requests.get(
            f"http://localhost:7008/api/EventVolunteers/closestVolunteers?eventLat= {eventLat}&eventLon={eventLon}"
        ).json()
        return volunteersRoute
