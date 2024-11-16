from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt
from entities.event import Event
from PySide6.QtCore import Signal


class EventListView(QWidget):
    showEventDetailsClicked = Signal(Event)
    showEventClicked = Signal()
    removeEventClicked = Signal(Event)

    def __init__(self):
        super().__init__()

        # Event list data (e.g., store event names and details)
        self.eventList = []

        # Initialize UI components
        self.init_ui()

        # Load custom stylesheet (if exists)
        self.apply_stylesheet("views/styles/eventList.qss")

    def init_ui(self):
        # Set up the main layout
        layout = QVBoxLayout()

        # Create the QListWidget to hold the event items
        self.listWidget = QListWidget()

        # Add the list widget to the main layout
        layout.addWidget(self.listWidget)

        # Set the layout for the widget
        self.setLayout(layout)
        self.setWindowTitle("Styled Event List")
        self.resize(400, 500)

    def apply_stylesheet(self, filename):
        stylesheet = self.load_stylesheet(filename)
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def load_stylesheet(self, filename):
        try:
            with open(filename, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Stylesheet {filename} not found.")
            return ""

    def add_custom_item(self, event: Event):
        # Create a QListWidgetItem (this is the container for each row)
        listItem = QListWidgetItem(self.listWidget)

        # Create a custom widget using the event instance
        itemWidget = self.create_item_widget(event, listItem)

        # Set the size hint of the list item based on the custom widget size
        listItem.setSizeHint(itemWidget.sizeHint())

        # Add the custom widget to the QListWidget's item
        self.listWidget.setItemWidget(listItem, itemWidget)

    def create_item_widget(self, event: Event, list_item: QListWidgetItem):
        # Create a custom widget to hold the item label and buttons
        itemWidget = QWidget()
        itemWidget.setObjectName("customItem")

        # Create a vertical layout for the custom widget to stack labels and buttons
        itemLayout = QVBoxLayout()
        itemLayout.setContentsMargins(5, 5, 5, 5)  # Better spacing

        # Create labels for each attribute of the event
        idLabel = QLabel(f"ID: {event.id}")
        descriptionLabel = QLabel(f"Description: {event.description}")
        locationLabel = QLabel(
            f"Location: {round(event.geoPoint.latitude, 4)}, {round(event.geoPoint.longitude, 4)}"
        )
        timeLabel = QLabel(f"Time: {event.time}")
        # Align labels
        idLabel.setAlignment(Qt.AlignLeft)
        descriptionLabel.setAlignment(Qt.AlignLeft)
        locationLabel.setAlignment(Qt.AlignLeft)
        timeLabel.setAlignment(Qt.AlignLeft)

        # Create a horizontal layout for the labe
        labelLayout = QHBoxLayout()
        labelLayout.addWidget(idLabel)
        labelLayout.addWidget(locationLabel)
        labelLayout.addWidget(timeLabel)

        descriptionLayout = QHBoxLayout()
        descriptionLayout.addWidget(descriptionLabel)

        # Add the labels to the item layout
        itemLayout.addLayout(labelLayout)
        itemLayout.addLayout(descriptionLayout)

        # Create a horizontal layout for the buttons
        buttonLayout = QHBoxLayout()

        # Create the "Show" button
        showButton = QPushButton("handle")
        showButton.clicked.connect(
            lambda: self.show_item(event, showButton)
        )  # Pass event to show_item
        showButton.setObjectName("showButton")

        # Create the "Remove" button
        removeButton = QPushButton("Remove")
        removeButton.clicked.connect(
            lambda: self.remove_item(list_item, event)
        )  # Pass event to remove_item
        removeButton.setObjectName("removeButton")

        buttonLayout.setContentsMargins(5, 5, 5, 5)  # Set margins for the QHBoxLayout

        # Add buttons to the button layout
        buttonLayout.addWidget(showButton)
        buttonLayout.addWidget(removeButton)
        buttonLayout.setAlignment(Qt.AlignRight)

        # Add the button layout to the main item layout
        itemLayout.addLayout(buttonLayout)

        # Set the layout for the custom widget
        itemWidget.setLayout(itemLayout)

        return itemWidget

    def show_item(self, event: Event, show_button: QPushButton):
        print(
            f"Showing event details:\n"
            f"ID: {event.id}\n"
            f"Description: {event.description}\n"
            f"Address: {event.address}\n"
            f"Time: {event.time}\n"
            f"Status: {event.status}\n"
        )
        event.status = "Handled"
        show_button.setText("Show again")
        show_button.setStyleSheet("background-color: #03a109; width: 80px;")
        self.showEventDetailsClicked.emit(event)
        self.showEventClicked.emit()

    def remove_item(self, list_item, event: Event):
        row = self.listWidget.row(list_item)
        self.listWidget.takeItem(row)
        print(f"Event '{event.description}' has been removed.")
        self.removeEventClicked.emit(event)
