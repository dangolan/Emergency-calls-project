
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class EventListView(QWidget):
    def __init__(self):
        super().__init__()
       # Create a layout to center the label
        layout = QVBoxLayout()

        # Create the label and center it
        label = QLabel("Event List View")
        label.setStyleSheet("font-size: 24px; color: black;")   
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")