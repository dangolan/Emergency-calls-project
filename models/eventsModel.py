
import requests

class EventsModel():
    def __init__(self):
        pass
    
    def get_routs_for_volunteers(self, eventLat, eventLon):
        url = f"http://localhost:7008/api/EventVolunteers/closestVolunteers?eventLat={eventLat}&eventLon={eventLon}"
        response = requests.get(url)
        return response
        
    