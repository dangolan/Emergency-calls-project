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
        self.list_widget = QListWidget()

        # Add the list widget to the main layout
        layout.addWidget(self.list_widget)

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
        list_item = QListWidgetItem(self.list_widget)

        # Create a custom widget using the event instance
        item_widget = self.create_item_widget(event, list_item)

        # Set the size hint of the list item based on the custom widget size
        list_item.setSizeHint(item_widget.sizeHint())

        # Add the custom widget to the QListWidget's item
        self.list_widget.setItemWidget(list_item, item_widget)

    def create_item_widget(self, event: Event, list_item: QListWidgetItem):
        # Create a custom widget to hold the item label and buttons
        item_widget = QWidget()
        item_widget.setObjectName("customItem")

        # Create a vertical layout for the custom widget to stack labels and buttons
        item_layout = QVBoxLayout()
        item_layout.setContentsMargins(5, 5, 5, 5)  # Better spacing

        # Create labels for each attribute of the event
        id_label = QLabel(f"ID: {event.id}")
        description_label = QLabel(f"Description: {event.description}")
        address_label = QLabel(f"Address: {event.address}\n")
        time_label = QLabel(f"Time: {event.time}")
        status_label = QLabel(f"Status: {event.status}")

        # Align labels
        id_label.setAlignment(Qt.AlignLeft)
        description_label.setAlignment(Qt.AlignLeft)
        address_label.setAlignment(Qt.AlignLeft)
        time_label.setAlignment(Qt.AlignLeft)
        status_label.setAlignment(Qt.AlignLeft)

        # Create a horizontal layout for the labe
        label_layout = QHBoxLayout()
        label_layout.addWidget(id_label)
        label_layout.addWidget(address_label)
        label_layout.addWidget(time_label)
        label_layout.addWidget(status_label)

        descriptionLayout = QHBoxLayout()
        descriptionLayout.addWidget(description_label)

        # Add the labels to the item layout
        item_layout.addLayout(label_layout)
        item_layout.addLayout(descriptionLayout)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create the "Show" button
        show_button = QPushButton("Show")
        show_button.clicked.connect(
            lambda: self.show_item(event)
        )  # Pass event to show_item
        show_button.setObjectName("showButton")

        # Create the "Remove" button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(
            lambda: self.remove_item(list_item, event)
        )  # Pass event to remove_item
        remove_button.setObjectName("removeButton")

        button_layout.setContentsMargins(5, 5, 5, 5)  # Set margins for the QHBoxLayout

        # Add buttons to the button layout
        button_layout.addWidget(show_button)
        button_layout.addWidget(remove_button)
        button_layout.setAlignment(Qt.AlignRight)

        # Add the button layout to the main item layout
        item_layout.addLayout(button_layout)

        # Set the layout for the custom widget
        item_widget.setLayout(item_layout)

        return item_widget

    def show_item(self, event: Event):
        print(
            f"Showing event details:\n"
            f"ID: {event.id}\n"
            f"Description: {event.description}\n"
            f"Address: {event.address}\n"
            f"Time: {event.time}\n"
            f"Status: {event.status}\n"
        )
        self.showEventDetailsClicked.emit(event)
        self.showEventClicked.emit()

    def remove_item(self, list_item, event: Event):
        row = self.list_widget.row(list_item)
        self.list_widget.takeItem(row)
        print(f"Event '{event.description}' has been removed.")
        self.removeEventClicked.emit(event)
