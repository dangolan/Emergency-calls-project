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
from eventSimulator import EmergencyEventSimulator
from models.eventsModel import EventsModel
from models.volunteersModel import VolunteersModel
import asyncio
from PySide6.QtCore import QEventLoop



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
    # Create models
    eventsModel = EventsModel()
    volunteersModel = VolunteersModel()
    # Create controllers
    shellController = ShellController(shellView)
    eventContoller = EventsController(
        eventsDetailView,
        eventsListView,
        closestVolunteerView,
        newEventsView,
        mapView,
        eventsModel
    )

    eventContoller.add_observer_to_show_event(shellController.show_map_and_event)
    eventContoller.errorSignal.connect(shellController.error)
    simulator = EmergencyEventSimulator(5)
    simulator.add_event.connect(eventContoller.add_event)
    simulator.start()

    shellView.show()

    sys.exit(app.exec())
    


if __name__ == "__main__":
    main()
