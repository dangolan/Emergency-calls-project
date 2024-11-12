from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class EventDetailsView(QWidget):
    def __init__(self):
        super().__init__()

        # create a layout
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setObjectName("eventDetailsLabel")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Load custom stylesheet (if exists)
        self.load_stylesheet("views/styles/newEvent.qss")


    def update_label(self, event):
        # Update label with new event details
        newText = (
            f"ID: {event.id}<br>"
            f"Time: {event.time}<br>"
            f"Status: {event.status}<br>"
            f"Location: {round(event.geoPoint.latitude, 4)}, {round(event.geoPoint.longitude, 4)}<br>"
            f"Description: {event.description}"
        )
        self.label.setText(newText)
    
    def load_stylesheet(self, file_path):
        with open(file_path, "r") as f:
            self.setStyleSheet(f.read())

        
