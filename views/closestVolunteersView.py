from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class ClosestVolunteersView(QWidget):
    def __init__(self):
        super().__init__()

        # create a layout
        layout = QVBoxLayout()

        # set the layout
        label = QLabel("Closest Volunteers 1")
        label.setStyleSheet("font-size: 24px; color: black;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        label = QLabel("Closest Volunteers 2")
        label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(label)
        label = QLabel("Closest Volunteers 3")
        label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(label)
        label = QLabel("Closest Volunteers 4")
        label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(label)
        label = QLabel("Closest Volunteers 5")
        label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(label)

        self.setLayout(layout)

        self.setStyleSheet("background-color: white;")
