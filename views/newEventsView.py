from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class NewEventsView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout to center the label
        layout = QVBoxLayout()
        label = QLabel()

        # Create the label and center it
        label.setText(
            "ID: 12345<br>"
            "Time: 10:00 AM<br>"
            "Status: Active<br>"
            "Location: Main Hall<br>"
            "Description: Event description goes here"
        )

        # Style the label
        label.setStyleSheet("font-size: 18px; color: black;")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

    def update_label(self, new_text):
        self.label.setText(new_text)
