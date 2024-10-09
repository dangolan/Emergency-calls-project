
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class ClosestVolunteersView(QWidget):
    def __init__(self):
        super().__init__()

        #create a layout
        layout = QVBoxLayout()

        #set the layout
        label = QLabel("Closest Volunteers")
        label.setStyleSheet("font-size: 24px; color: black;")   
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)

        self.setStyleSheet("background-color: white;")


       
       
