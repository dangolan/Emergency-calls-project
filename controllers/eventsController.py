
from worker import Worker



class EventsController:
    def __init__(
        self,
        eventsDetailView=None,
        eventsListView=None,
        closestVolunteerView=None,
        newEventsView=None,
        mapView=None,
        eventsModel=None
    ):
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
        print("New event received:", event)
        self.newEventsView.update_label(event)
        self.eventsListView.add_custom_item(event)

    def create_map(self, event):
        self.mapView.show_preloader()
        # Call the async function and wait for the result
        def show_map(volunteers):
            if volunteers:
                # Draw the map with the route
                self.mapView.hide_preloader()
                self.mapView.draw_map(volunteers, event.geoPoint.latitude, event.geoPoint.longitude)
                self.closestVolunteerView.clear()
                self.closestVolunteerView.add_volunteers(volunteers)
            else:
                # Draw the map without the route
                self.mapView.draw_map([], event.geoPoint.latitude, event.geoPoint.longitude)
                print("No volunteers found")

        worker = Worker(lambda: self.eventsModel.get_routs_for_volunteers(event.geoPoint.latitude, event.geoPoint.longitude))
        worker.result_signal.connect(show_map)
        worker.error_signal.connect(print)
        worker.start()
    
    
    def add_observer_to_show_event(self, action):
        self.eventsListView.showEventClicked.connect(action)

