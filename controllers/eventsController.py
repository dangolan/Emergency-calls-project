from eventSimulator import EmergencyEventSimulator


class EventsController:
    def __init__(
        self,
        eventsDetailView=None,
        eventsListView=None,
        closestVolunteerView=None,
        newEventsView=None,
    ):
        self.newEventsView = newEventsView
        self.eventsDetailView = eventsDetailView
        self.eventsListView = eventsListView
        self.closestVolunteerView = closestVolunteerView
        self.newEventsView = newEventsView

    def add_event(self, event):
        # This function will be called by the simulator with each new event
        print("New event received:", event)
        self.newEventsView.update_label(event)
        self.eventsListView.add_custom_item(event)
