from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from entities.event import Event


class NewEventsView(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize label and layout
        self.layout = QVBoxLayout()
        self.label = QLabel()

        # Set initial text for the label

        # Style the label
        self.label.setStyleSheet("font-size: 12px; color: black;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.label)

        # Set layout and background color
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: white;")

    def update_label(self, event):
        # Update label with new event details
        new_text = (
            f"ID: {event.id}<br>"
            f"Time: {event.time}<br>"
            f"Status: {event.status}<br>"
            f"Location: {event.address}<br>"
            f"Description: {event.description}"
        )
        self.label.setText(new_text)
