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

        # Initialize the central widget and main layout
        self.init_central_widget()

        # Initialize the toolbar
        self.init_toolbar()

        # Initialize the buttons
        self.init_buttons()

        # Initialize the views
        self.init_views(
            mapView,
            eventsListView,
            volunteersListView,
            eventsDetailView,
            closestVolunteerView,
            newEventsView,
        )

        # Initialize the status bar
        self.init_status_bar()
        #set stylesheet
        stylesheet = self.load_stylesheet("views/styles/shell.qss")
        self.setStyleSheet(stylesheet)

    def init_central_widget(self):
        # Create the main grid layout for the window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        # Set geometry
        self.setGeometry(100, 100, 1000, 850)

    def init_toolbar(self):
        # Add a toolbar
        self.toolbar = self.addToolBar("Main")
        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(80)
        stylesheet = self.load_stylesheet("views/styles/toolBar.qss")
        self.toolbar.setStyleSheet(stylesheet)

        # Create a spacer widget to push the back button to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Create the Back button
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon("images/goBack.png"))  # Set your back arrow icon
        self.backButton.setIconSize(QSize(24, 24))  # Set the icon size
        # Connect the Back button to its signal
        self.backButton.clicked.connect(self.goBackClicked.emit)

        # Add the Back button to the toolbar
        self.toolbar.addWidget(self.backButton)

    def init_buttons(self):
        # Create the buttons
        self.showEventsButton = QPushButton("Show Events")
        self.showEventsButton.setObjectName("showEventsButton")
        self.showVolunteersButton = QPushButton("Show Volunteers")
        self.showVolunteersButton.setObjectName("showVolunteersButton")

        # Connect the buttons to their respective signals
        self.showEventsButton.clicked.connect(self.showEventsClicked.emit)
        self.showVolunteersButton.clicked.connect(self.showVolunteersClicked.emit)

        # Add buttons to the main layout
        self.main_layout.addWidget(self.showEventsButton, 1, 0, 1, 2)
        self.main_layout.addWidget(self.showVolunteersButton, 2, 0, 1, 2)

    def init_views(
        self,
        mapView,
        eventsListView,
        volunteersListView,
        eventsDetailView,
        closestVolunteerView,
        newEventsView,
    ):
        # Create a label to display the number of events
        self.newEventsView = newEventsView
        self.main_layout.addWidget(self.newEventsView, 0, 0, 1, 2)

        # Add the events list view
        self.eventsListView = eventsListView
        self.main_layout.addWidget(self.eventsListView, 0, 2, 6, 4)

        # Add the volunteers list view
        self.volunteersListView = volunteersListView
        self.main_layout.addWidget(self.volunteersListView, 0, 2, 6, 4)

        # Add the map view
        self.mapView = mapView
        self.main_layout.addWidget(self.mapView, 0, 2, 4, 4)

        self.eventsListView.hide()
        self.volunteersListView.hide()

        # Add the event detail view
        self.eventsDetailView = eventsDetailView
        self.main_layout.addWidget(self.eventsDetailView, 4, 2, 2, 4)

        # Add the closest volunteer view
        self.closestVolunteerView = closestVolunteerView
        self.main_layout.addWidget(self.closestVolunteerView, 3, 0, 3, 2)

    def init_status_bar(self):
        # Add a status bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Status bar message")
        self.statusBar.setStyleSheet("background-color: black; color: white;")

    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()

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