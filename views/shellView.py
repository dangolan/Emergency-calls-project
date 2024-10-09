from PySide6.QtWidgets import QWidget, QGridLayout, QMainWindow, QLabel, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt


# Define the ShellView class in its own view
class ShellView(QMainWindow):
    # Signals at class level
    showEventsClicked = Signal()
    showVolunteersClicked = Signal()

    def __init__(self, mapView, eventsListView, volunteersListView, eventsDetailView, closestVolunteerView):
        super().__init__()


        # Create the main grid layout for the window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        # Set geometry
        self.setGeometry(100, 100, 800, 600)

        #add a tool bar
        self.toolbar = self.addToolBar("Main")

        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(50)
        self.toolbar.setStyleSheet("background-color: black;")

        label = QLabel("tool bar")
        self.toolbar.addWidget(label)

        #Create the buttons
        self.showEventsButton = QPushButton("Show Events")
        self.showVolunteersButton = QPushButton("Show Volunteers")

        # Connect the buttons to their respective signals
        self.showEventsButton.clicked.connect(self.showEventsClicked.emit)
        self.showVolunteersButton.clicked.connect(self.showVolunteersClicked.emit)

        # Set different background colors for the buttons
        self.showEventsButton.setStyleSheet("background-color: lightblue; color: black;")
        self.showVolunteersButton.setStyleSheet("background-color: lightgreen; color: black;")



        #add label of number of events to the grid layout
        self.numberOfEventsLabel = QLabel("New Events: 0")
        self.numberOfEventsLabel.setStyleSheet("font-size: 12px; color: white;")
        self.numberOfEventsLabel.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.numberOfEventsLabel, 1, 0, 1, 2)
        
        #add the side bar view to the grid layout
        #main_layout.addWidget(self.sideBarView, 0, 0, 1, 2)

        #add a button to the main layout
        main_layout.addWidget(self.showEventsButton, 0, 0, 1, 1)
        main_layout.addWidget(self.showVolunteersButton, 0, 1, 1, 1)

        # Add the events list view (connect with the sidebar later)
        self.eventsListView = eventsListView
        main_layout.addWidget(self.eventsListView, 0, 2, 6, 4)

        # Add the volunteers list view (connect with the sidebar later)
        self.volunteersListView = volunteersListView
        main_layout.addWidget(self.volunteersListView, 0, 2, 6, 4)

        # Add the map view
        self.mapView = mapView
        main_layout.addWidget(self.mapView, 0, 2, 4, 4)

        self.eventsListView.hide()
        self.volunteersListView.hide()


        # Add the event detail view
        self.eventsDetailView = eventsDetailView
        main_layout.addWidget(self.eventsDetailView, 4, 2, 2, 4)


        # Add the closest volunteer view (connect with the map later)
        self.closestVolunteerView = closestVolunteerView
        main_layout.addWidget(self.closestVolunteerView, 2, 0, 4, 2)


        #add a status bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Status bar message")
        self.statusBar.setStyleSheet("background-color: black; color: white;")

    
    def show_events_list(self):
            self.eventsListView.show()
            self.mapView.hide()
            self.volunteersListView.hide()
            self.eventsDetailView.hide()

    def show_volunteers_list(self):
            self.volunteersListView.show()
            self.mapView.hide()
            self.eventsListView.hide()
            self.eventsDetailView.hide()

    def show_map_and_event(self):
            self.eventsListView.hide()
            self.volunteersListView.hide()
            self.mapView.show()
            self.eventsDetailView.show()


        


