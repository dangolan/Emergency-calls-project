
class EventsController:
    def __init__(self, eventsDetailView, eventsListView,closestVolunteerView, newEventsView):
        self.eventsDetailView = eventsDetailView
        self.eventsListView = eventsListView
        self.closestVolunteerView = closestVolunteerView
        self.newEventsView = newEventsView
        #self.eventsModel = eventsModel
