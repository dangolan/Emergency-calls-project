from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
class NewEventsView(QWidget):

    def __init__(self):
        super().__init__()
        # Initialize layouts
        self.mainLayout = QVBoxLayout()

        # Header label
        self.header = QLabel("incoming events")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setObjectName("header")
        self.mainLayout.addWidget(self.header)

        # Event details label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.label)

        # Set layout and load stylesheet
        self.setLayout(self.mainLayout)
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
