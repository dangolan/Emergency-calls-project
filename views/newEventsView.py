from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
class NewEventsView(QWidget):

    def __init__(self):
        super().__init__()
        

        # Initialize layouts
        self.main_layout = QVBoxLayout()

        # Header label
        self.header = QLabel("incoming events")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setObjectName("header")
        self.main_layout.addWidget(self.header)


        # Event details label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.label)

        

        # Set layout and load stylesheet
        self.setLayout(self.main_layout)
        self.load_stylesheet("views/styles/newEvent.qss")

    def update_label(self, event):
        # Update label with new event details
        new_text = (
            f"ID: {event.id}<br>"
            f"Time: {event.time}<br>"
            f"Status: {event.status}<br>"
            f"Location: {round(event.geoPoint.latitude, 4)}, {round(event.geoPoint.longitude, 4)}<br>"
            f"Description: {event.description}"
        )
        self.label.setText(new_text)

    def load_stylesheet(self, file_path):
        with open(file_path, "r") as f:
            self.setStyleSheet(f.read())
