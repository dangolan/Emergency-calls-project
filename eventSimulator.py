import random
from threading import Thread
import time
from PySide6.QtCore import QObject, Signal
from entities.event import Event


class EmergencyEventSimulator(QObject):
    add_event = Signal(Event)

    def __init__(self, interval=6):  # Corrected __init_ method
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

    def generate_event(self):
        event_id = random.randint(1000, 9999)
        event_type = random.choice(self.events)
        location = f"Location_{random.randint(1, 100)}"
        status = "Pending"
        description = f"{event_type} reported at {location}"

        # Assuming latitude and longitude for the event, you can replace with actual values
        latitude = random.uniform(
            32.0, 32.1
        )  # Random latitude in the range of Tel Aviv
        longitude = random.uniform(
            34.75, 34.85
        )  # Random longitude in the range of Tel Aviv
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
