import requests
from entities.volunteer import Volunteer
from entities.eventVolunteer import EventVolunteer
from typing import List
from entities.event import Event


class EventsModel:
    def __init__(self):
        self.events : List[Event] = []

    # Add event to the list of events
    def add_event(self, event : Event):
        self.events.append(event)
    # Remove event from the list of events
    def remove_event(self, id):
        self.events = [event for event in self.events if event.id != id]
    # Get all events
    def get_events(self):
        return self.events
    # Set event status as handled
    def set_event_as_handled(self, id):
        for event in self.events:
            if event.id == id:
                event.status = "Handled"
    # Get volunteers for the event
    def get_routs_for_volunteers(self, eventLat, eventLon):
        # Construct the URL with event latitude and longitude
        url = f"http://localhost:7008/api/EventVolunteers/closestVolunteers?eventLat={eventLat}&eventLon={eventLon}"
        response = requests.get(url)
        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            # Parse the response into a list of EventVolunteer objects
            return self.parse_response_to_event_volunteers(response_data)
        else:
            # Handle error case as needed, such as logging or raising an exception
            raise Exception(
                f"Failed to get volunteers. Status code: {response.status_code} - {response.text}"
            )
    # Parse the response into a list of EventVolunteer objects
    def parse_response_to_event_volunteers(self, response_data):
        eventVolunteers = []
        for item in response_data:
            volData = item["volunteer"]
            volunteer = Volunteer(
                id=volData["id"],
                uniqueIdNumber=volData["uniqueIdNumber"],
                firstName=volData["firstName"],
                lastName=volData["lastName"],
                phone=volData["phone"],
                latitude=volData["latitude"],
                longitude=volData["longitude"],
                city=volData["city"],
                street=volData["street"],
                houseNumber=volData["houseNumber"],
                imageUrl=volData["photoUrl"],
            )

            # Create EventVolunteer instance
            eventVolunteer = EventVolunteer(
                volunteer=volunteer,
                distance=item["distance"],
                duration=item["duration"],
                routeCoordinates=item["routeCoordinates"],
            )

            eventVolunteers.append(eventVolunteer)

        return eventVolunteers
