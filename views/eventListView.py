from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from entities.event import Event
from PySide6.QtCore import Signal
from typing import List


class EventListView(QWidget):
    showEventDetailsClicked = Signal(Event)
    showEventClicked = Signal()
    removeEventClicked = Signal(Event)

    def __init__(self):
        super().__init__()
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
        itemWidget = self.create_item_widget(event)

        # Set the size hint of the list item based on the custom widget size
        listItem.setSizeHint(itemWidget.sizeHint())

        # Add the custom widget to the QListWidget's item
        self.listWidget.setItemWidget(listItem, itemWidget)

    def create_item_widget(self, event: Event):
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
        if event.status == "Handled":
            showButton = QPushButton("Handled")
            showButton.setText("Show again")
            showButton.setStyleSheet("background-color: #03a109; width: 80px;")
        else:
            showButton = QPushButton("handle")
        showButton.clicked.connect(
            lambda: self.show_item(event)
        )  # Pass event to show_item
        showButton.setObjectName("showButton")

        # Create the "Remove" button
        removeButton = QPushButton("Remove")
        removeButton.clicked.connect(
            lambda: self.remove_item(event)
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

    def show_item(self, event: Event):
        self.showEventDetailsClicked.emit(event)
        self.showEventClicked.emit()
    
    def set_events(self, events : List[Event]):
        self.listWidget.clear()
        for event in events:
            self.add_custom_item(event)

    def remove_item(self, event: Event):
        self.removeEventClicked.emit(event)
