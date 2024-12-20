import sys
from PySide6.QtWidgets import QApplication
from views.mapView import MapView
from views.eventListView import EventListView
from views.volunteersListView import VolunteersListView
from views.eventDetailsView import EventDetailsView
from views.closestVolunteersView import ClosestVolunteersView
from views.shellView import ShellView
from controllers.shellController import ShellController
from views.newEventsView import NewEventsView
from views.addVolunteerView import AddVolunteerView
from controllers.eventsController import EventsController
from eventSimulator import EmergencyEventSimulator
from models.eventsModel import EventsModel
from models.volunteersModel import VolunteersModel
from controllers.volunteersListController import VolunteersListController


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
    # Create a view for adding a new volunteer
    addVolunteerView = AddVolunteerView()
    # Create a shell view
    shellView = ShellView(
        mapView,
        eventsListView,
        volunteersListView,
        eventsDetailView,
        closestVolunteerView,
        newEventsView,
        addVolunteerView,
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
        eventsModel,
    )
    volunteerController = VolunteersListController(
        volunteersListView, volunteersModel, addVolunteerView
    )

    # Connect signals for switching views
    # Connect the swich view in the shellController to the volunteerController
    volunteerController.add_observer_to_add_volunteer(
        shellController.show_add_volunteer
    )
    # add observer for switching views
    eventContoller.add_observer_to_show_event(shellController.show_map_and_event)

    # Connect the error signals
    # Connect the error func in shellController to the error signal in eventController
    volunteerController.errorSignal.connect(shellController.error)
    # Connect the error func in shellController to the error signal in eventController
    eventContoller.errorSignal.connect(shellController.error)

    # Create an event simulator
    simulator = EmergencyEventSimulator(10)
    # Connect the add_event signal to the eventController
    simulator.add_event.connect(eventContoller.add_event)
    simulator.start()

    shellView.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
