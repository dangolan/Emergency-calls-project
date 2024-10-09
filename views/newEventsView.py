from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class NewEventsView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout to center the label
        self.layout = QVBoxLayout()

        # Create the label and center it
        self.label = QLabel("New Events View")
        self.label.setStyleSheet("font-size: 24px; color: black;")   
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

    def update_label(self, new_text):
        self.label.setText(new_text)