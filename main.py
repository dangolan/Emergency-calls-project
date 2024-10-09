import sys
from PySide6.QtWidgets import QApplication, QWidget
from views.mapView import MapView
from views.eventListView import EventListView
from views.volunteersListView import VolunteersListView
from views.eventDetailsView import EventDetailsView
from views.closestVolunteersView import ClosestVolunteersView
from views.shellView import ShellView
from controllers.shellController import ShellController

def main():
    app = QApplication(sys.argv)

    mapView = MapView()
    eventsListView = EventListView()
    volunteersListView = VolunteersListView()
    eventsDetailView = EventDetailsView()
    closestVolunteerView = ClosestVolunteersView()

    shellView = ShellView(mapView, eventsListView, volunteersListView, eventsDetailView, closestVolunteerView)
    ShellController(shellView)

    shellView.show()

    app.exec()

if __name__ == "__main__":
    main()