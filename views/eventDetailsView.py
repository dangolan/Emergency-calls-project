from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class EventDetailsView(QWidget):
    def __init__(self):
        super().__init__()

        # create a layout
        layout = QVBoxLayout()
        label = QLabel()

        # set the layout

        label.setText(
            "ID: 12345<br>"
            "Time: 10:00 AM<br>"
            "Status: Active<br>"
            "Location: Main Hall<br>"
            "Description: Event description goes here"
        )

        # Style the label
        label.setStyleSheet("font-size: 14px; color: black;")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        self.setLayout(layout)

        self.setStyleSheet("background-color: white;")
