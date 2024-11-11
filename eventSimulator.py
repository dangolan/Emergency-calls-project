import random
from threading import Thread
import time
from PySide6.QtCore import QObject, Signal
from entities.event import Event


class EmergencyEventSimulator(QObject):
    add_event = Signal(Event)

    def __init__(self, interval=10000):  # Corrected __init_ method
        super().__init__()
        self.interval = interval
        self.running = False

        self.events = [
            "accident",
            "fire",
            "medical emergency",
            "theft",
            "natural disaster",
        ]
    def generate_random_coordinates_in_tel_aviv(self):
        # Define the Tel Aviv area with a more specific coordinate range
        lat_range = (32.0500, 32.1200)  # Narrower latitude range for Tel Aviv
        lon_range = (34.7600, 34.8200)  # Narrower longitude range for Tel Aviv

        return (
            random.uniform(lat_range[0], lat_range[1]),  # latitude
            random.uniform(lon_range[0], lon_range[1])   # longitude
        )

    def generate_event(self):
        event_id = random.randint(1000, 9999)
        event_type = random.choice(self.events)
        location = f"Location_{random.randint(1, 100)}"
        status = "Pending"
        description = f"{event_type} reported at {location}"

        latitude, longitude = self.generate_random_coordinates_in_tel_aviv()
        address = location  # Could be refined with actual address data

        event_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Returning an instance of the Event class
        return Event(
            event_id, description, latitude, longitude, address, event_time, status
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
