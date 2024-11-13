from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QListWidgetItem,
    QLabel,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal
from entities.volunteer import Volunteer
from PySide6.QtCore import QSize


class VolunteersListView(QWidget):
    # Define signals to emit the volunteer for remove and update actions
    remove_volunteer_signal = Signal(Volunteer)
    update_volunteer_signal = Signal(Volunteer)

    def __init__(self):
        super().__init__()

        # set stylesheet
        stylesheet = self.load_stylesheet("views/styles/volunteersList.qss")
        self.setStyleSheet(stylesheet)

        # Main list widget to display volunteers
        self.volunteer_list_widget = QListWidget()

        # Main layout for the entire view
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.volunteer_list_widget)
        self.setLayout(main_layout)
        # volunteers = [
        #     Volunteer(
        #         id=1,
        #         firstName="John",
        #         lastName="Doe",
        #         phone="123-456-7890",
        #         latitude=34.0522,
        #         longitude=-118.2437,
        #         city="Los Angeles",
        #         street="Main Street",
        #         houseNumber="100",
        #         imageUrl="path/to/image1.jpg",
        #     )
        # ]
        # for volunteer in volunteers:
        #     self.add_volunteer(volunteer)

    def add_volunteer(self, volunteer: Volunteer):
        # Create a custom widget to hold volunteer information
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)

        # Add the image as an icon
        icon_label = QLabel()
        pixmap = QIcon(volunteer.imageUrl).pixmap(
            QSize(50, 50)
        )  # Adjust size as needed
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

        # Display the volunteer's name
        name_label = QLabel(f"{volunteer.firstName} {volunteer.lastName}")
        layout.addWidget(name_label)

        # Create a remove button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.emit_remove(volunteer))
        layout.addWidget(remove_button)

        # Create an update button
        update_button = QPushButton("Update")
        update_button.clicked.connect(lambda: self.emit_update(volunteer))
        layout.addWidget(update_button)

        # Add custom widget to the QListWidget using QListWidgetItem
        list_item = QListWidgetItem(self.volunteer_list_widget)
        list_item.setSizeHint(
            item_widget.sizeHint()
        )  # Ensure the item has enough space
        self.volunteer_list_widget.setItemWidget(list_item, item_widget)

    def emit_remove(self, volunteer):
        """Emit the remove signal with the selected volunteer."""
        self.remove_volunteer_signal.emit(volunteer)

    def emit_update(self, volunteer):
        """Emit the update signal with the selected volunteer."""
        self.update_volunteer_signal.emit(volunteer)

    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()
