from worker import Worker
from PySide6.QtCore import Signal, QObject


class EventsController(QObject):
    errorSignal = Signal(str)

    def __init__(
        self,
        eventsDetailView=None,
        eventsListView=None,
        closestVolunteerView=None,
        newEventsView=None,
        mapView=None,
        eventsModel=None,
    ):
        super().__init__()
        self.newEventsView = newEventsView
        self.eventsDetailView = eventsDetailView
        self.eventsListView = eventsListView
        self.closestVolunteerView = closestVolunteerView
        self.newEventsView = newEventsView
        self.mapView = mapView
        self.eventsModel = eventsModel
        self.eventsListView.showEventDetailsClicked.connect(self.create_map)
        self.mapView.draw_map([], 32.0853, 34.7818)

    def add_event(self, event):
        # This function will be called by the simulator with each new event
        print(
            "New event received:",
            event.id,
            event.geoPoint.latitude,
            event.geoPoint.longitude,
            event.description,
            event.time,
        )
        self.newEventsView.update_label(event)
        self.eventsListView.add_custom_item(event)

    def create_map(self, event):
        self.mapView.show_preloader()
        self.closestVolunteerView.show_preloader()
        self.eventsDetailView.update_label(event)

        # Call the async function and wait for the result
        def show_map(eventVolunteers):
            if eventVolunteers:
                # Draw the map with the route
                self.mapView.hide_preloader()
                self.closestVolunteerView.hide_preloader()
                self.mapView.draw_map(
                    eventVolunteers, event.geoPoint.latitude, event.geoPoint.longitude
                )
                self.closestVolunteerView.clear()
                self.closestVolunteerView.add_volunteers(eventVolunteers)
            else:
                # Draw the map without the route
                self.mapView.hide_preloader()
                self.closestVolunteerView.hide_preloader()
                self.mapView.draw_map(
                    [], event.geoPoint.latitude, event.geoPoint.longitude
                )
                print("No volunteers found")

        # Create a worker to call the async function
        worker = Worker(
            lambda: self.eventsModel.get_routs_for_volunteers(
                event.geoPoint.latitude, event.geoPoint.longitude
            )
        )
        worker.result_signal.connect(show_map)
        worker.error_signal.connect(self.error)
        worker.start()

    # Add observer to show event
    def add_observer_to_show_event(self, action):
        self.eventsListView.showEventClicked.connect(action)

    # Error function to pass error messages to the main thread
    def error(self, message):
        print(message)
        self.mapView.hide_preloader()
        self.errorSignal.emit(message)
