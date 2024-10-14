from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QMainWindow,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon


# Define the ShellView class in its own view
class ShellView(QMainWindow):
    # Signals at class level
    showEventsClicked = Signal()
    showVolunteersClicked = Signal()
    goBackClicked = Signal()

    def __init__(
        self,
        mapView,
        eventsListView,
        volunteersListView,
        eventsDetailView,
        closestVolunteerView,
        newEventsView,
    ):
        super().__init__()

        # Create the main grid layout for the window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        # Set geometry
        self.setGeometry(100, 100, 900, 700)

        # add a tool bar
        self.toolbar = self.addToolBar("Main")

        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(60)
        self.toolbar.setStyleSheet("background-color: black;")

        # Create a spacer widget to push the back button to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Create the Back button
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon("images\go_back.png"))  # Set your back arrow icon
        self.backButton.setIconSize(QSize(24, 24))  # Set the icon size
        self.backButton.setStyleSheet(
            "background-color: transparent; border: None;"
        )  # Make the background transparent
        # Connect the Back button to its signal (you'll define the method to handle the back action)
        self.backButton.clicked.connect(self.goBackClicked.emit)

        # Add the Back button to the toolbar
        self.toolbar.addWidget(self.backButton)

        # Create the buttons
        self.showEventsButton = QPushButton("Show Events")
        self.showVolunteersButton = QPushButton("Show Volunteers")

        # Connect the buttons to their respective signals
        self.showEventsButton.clicked.connect(self.showEventsClicked.emit)
        self.showVolunteersButton.clicked.connect(self.showVolunteersClicked.emit)

        # Set different background colors for the buttons
        self.showEventsButton.setStyleSheet(
            "background-color: lightblue; color: black;"
        )
        self.showVolunteersButton.setStyleSheet(
            "background-color: lightgreen; color: black;"
        )

        label = QLabel("tool bar")
        self.toolbar.addWidget(label)

        # Create a label to display the number of events
        self.newEventsView = newEventsView
        main_layout.addWidget(self.newEventsView, 0, 0, 1, 2)

        # add a button to the main layout
        main_layout.addWidget(self.showEventsButton, 1, 0, 1, 2)
        main_layout.addWidget(self.showVolunteersButton, 2, 0, 1, 2)

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
        main_layout.addWidget(self.closestVolunteerView, 3, 0, 3, 2)

        # add a status bar
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
