import sys
from PySide6.QtWidgets import QApplication, QWidget
from views.mapView import MapView
from views.eventListView import EventListView
from views.volunteersListView import VolunteersListView
from views.eventDetailsView import EventDetailsView
from views.closestVolunteersView import ClosestVolunteersView
from views.shellView import ShellView
from controllers.shellController import ShellController
from views.newEventsView import NewEventsView
from controllers.eventsController import EventsController
from PySide6.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    # Create a map view
    mapView = MapView()
    # Create an event list view
    eventsListView = EventListView()
    # Create a volunteers list view
    volunteersListView = VolunteersListView()
    # Create an event details view
    eventsDetailView = EventDetailsView()
    # Create a closest volunteers view
    closestVolunteerView = ClosestVolunteersView()
    # Create a View for showing new events
    newEventsView = NewEventsView()
    # Create a shell view
    shellView = ShellView(
        mapView,
        eventsListView,
        volunteersListView,
        eventsDetailView,
        closestVolunteerView,
        newEventsView,
    )
    # Create controllers
    ShellController(shellView)
    EventsController(
        eventsDetailView, eventsListView, closestVolunteerView, newEventsView
    )

    shellView.show()

    app.exec()


if __name__ == "__main__":
    main()
