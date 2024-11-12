import random
from threading import Thread
import time
from PySide6.QtCore import QObject, Signal
from entities.event import Event


class EmergencyEventSimulator(QObject):
    add_event = Signal(Event)

    def __init__(self, interval=10):  # Corrected __init_ method
        super().__init__()
        self.interval = interval
        self.running = False
        self.emergencyEvents = [
        "Fire in residential building",
        "Car accident on main highway",
        "Flooded road blocking traffic",
        "Medical emergency at school",
        "Gas leak reported downtown",
        "Power outage in city center",
        "Suspicious package at station",
        "Water main burst on street",
        "Tree fallen on busy road",
        "Small aircraft emergency landing",
        "Animal loose in public park",
        "Robbery in progress at bank",
        "Child lost in shopping mall",
        "Chemical spill near factory",
        "Public disturbance at stadium",
        "Severe weather alert issued",
        "Smoke reported in high-rise",
        "Vehicle collision at intersection",
        "Minor explosion in warehouse",
        "Fire alarm triggered in office",
        "Traffic signal malfunctioning",
        "Flooding in basement parking",
        "Elevator stuck with passengers",
        "Vandalism at city library",
        "Protest march blocking roads",
        "Unresponsive person at park",
        "Evacuation at shopping center",
        "Multiple injuries in bus crash",
        "Overcrowding at public event",
        "Downed power line on street",
        "Gas station fire in progress",
        "Shooting reported in neighborhood",
        "Animal rescue at construction site",
        "Rescue team needed for drowning",
        "Unattended bag in subway station",
        "Medical aid needed on highway",
        "Explosion heard near warehouse",
        "Firefighters needed at forest fire",
        "Drunk driver causing accidents",
        "Domestic disturbance in apartment",
        "Boat collision on city lake",
        "Carbon monoxide alarm triggered",
        "Flood evacuation needed urgently",
        "Hostage situation in progress",
        "Structural collapse at building",
        "Toxic smoke in industrial area",
        "Vehicle pileup on major road",
        "Person trapped under vehicle",
        "Pipeline rupture near city center",
        "Electrical fire in warehouse",
        "Crowd panic at sports event"
    ]
        self.counter = 0


    
    def generate_random_coordinates_in_tel_aviv(self):
        # Define the Tel Aviv area with a more specific coordinate range
        latRange = (32.0500, 32.1200)  # Narrower latitude range for Tel Aviv
        lonRange = (34.7600, 34.8200)  # Narrower longitude range for Tel Aviv

        return (
            random.uniform(latRange[0], latRange[1]),  # latitude
            random.uniform(lonRange[0], lonRange[1])   # longitude
        )

    def generate_event(self):

        # Increment the event counter
        self.counter += 1

        eventId = self.counter
        status = "Pending"
        description = random.choice(self.emergencyEvents)
        latitude, longitude = self.generate_random_coordinates_in_tel_aviv()
        address = ""
        eventTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Returning an instance of the Event class
        return Event(
            eventId, description, latitude, longitude, address, eventTime, status
        )

    def start(self):
        self.running = True
        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        while self.running:
            event = self.generate_event()
            if self.add_event:
                self.add_event.emit(event)
            time.sleep(self.interval)
