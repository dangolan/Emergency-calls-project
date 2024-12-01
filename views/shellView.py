from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QMainWindow,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, Qt


# Define the ShellView class in its own view
class ShellView(QMainWindow):
    # Signals at class level
    showEventsClicked = Signal()
    showVolunteersClicked = Signal()
    goBackClicked = Signal()
    addVolunteerClicked = Signal()

    def __init__(
        self,
        mapView,
        eventsListView,
        volunteersListView,
        eventsDetailView,
        closestVolunteerView,
        newEventsView,
        addVolunteerView,
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
            addVolunteerView,
        )

        # Initialize the status bar
        self.init_status_bar()
        # set stylesheet
        stylesheet = self.load_stylesheet("views/styles/shell.qss")
        self.setStyleSheet(stylesheet)

    def init_central_widget(self):
        # Create the main grid layout for the window
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.mainLayout = QGridLayout(centralWidget)

        # Set geometry
        self.setGeometry(100, 100, 1000, 600)

    def init_toolbar(self):
        # Add a toolbar
        self.toolbar = self.addToolBar("Main")
        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(80)
        stylesheet = self.load_stylesheet("views/styles/toolBar.qss")
        self.toolbar.setStyleSheet(stylesheet)

        # Create a label to display the logo
        label = QLabel(self)
        pixmap = QPixmap("images/logo.png")
        # Set the pixmap to the label
        label.setPixmap(pixmap.scaled(QSize(256, 256), Qt.KeepAspectRatio))

        # Add the label (with the image) to the toolbar
        self.toolbar.addWidget(label)

        # Create a spacer widget to push the back button to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Create the Back button
        self.backButton = QPushButton()
        self.backButton.setObjectName("backButton")
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
        self.mainLayout.addWidget(self.showEventsButton, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.showVolunteersButton, 2, 0, 1, 2)

    def init_views(
        self,
        mapView,
        eventsListView,
        volunteersListView,
        eventsDetailView,
        closestVolunteerView,
        newEventsView,
        addVolunteerView,
    ):
        # Create a label to display the number of events
        self.newEventsView = newEventsView
        self.mainLayout.addWidget(self.newEventsView, 0, 0, 1, 2)
        self.newEventsView.setObjectName("newEventsView")

        # Add the events list view
        self.eventsListView = eventsListView
        self.mainLayout.addWidget(self.eventsListView, 0, 2, 6, 4)

        # Add the volunteers list view
        self.volunteersListView = volunteersListView
        self.mainLayout.addWidget(self.volunteersListView, 0, 2, 6, 4)

        # Add the map view
        self.mapView = mapView
        self.mainLayout.addWidget(self.mapView, 0, 2, 5, 4)

        self.eventsListView.hide()
        self.volunteersListView.hide()

        # Add the event detail view
        self.eventsDetailView = eventsDetailView
        self.mainLayout.addWidget(self.eventsDetailView, 5, 2, 1, 4)

        # Add the closest volunteer view
        self.closestVolunteerView = closestVolunteerView
        self.mainLayout.addWidget(self.closestVolunteerView, 3, 0, 3, 2)

        # Add the add volunteer view
        self.addVolunteerView = addVolunteerView
        self.mainLayout.addWidget(self.addVolunteerView, 3, 0, 3, 2)

        self.addVolunteerView.hide()

    def init_status_bar(self):
        # Add a status bar
        self.statusBar = self.statusBar()
        self.statusBar.setStyleSheet("background-color: black; color: white;")

    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()

    def show_events_list(self):
        self.eventsListView.show()
        self.mapView.hide()
        self.addVolunteerView.hide()
        self.closestVolunteerView.show()
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
        self.addVolunteerView.hide()
        self.closestVolunteerView.show()
        self.mapView.show()
        self.eventsDetailView.show()

    def show_add_volunteer(self):
        self.addVolunteerView.show()
        self.closestVolunteerView.hide()
        print("show add volunteer")
