from typing import List
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QListWidgetItem,
    QLabel,
    QComboBox,
    QLineEdit,
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath, QMovie
from PySide6.QtCore import Qt, Signal
from entities.volunteer import Volunteer
from PySide6.QtCore import QTimer
from entities.listVolunteer import ListVolunteer


class VolunteersListView(QWidget):
    # Define signals to emit the volunteer for remove and update actions
    removeVolunteerSignal = Signal(Volunteer)
    updateVolunteerSignal = Signal(Volunteer)
    updateVolunteerClicked = Signal()
    addVolunteerClicked = Signal()

    def __init__(self):
        super().__init__()

        self.volunteers = []

        # Load and set stylesheet
        stylesheet = self.load_stylesheet("views/styles/volunteersList.qss")
        self.setStyleSheet(stylesheet)

        # Add a ComboBox for search type
        self.searchTypeComboBox = QComboBox()
        self.searchTypeComboBox.addItems(["Address", "ID", "Name"])

        # Add a QLineEdit for search
        self.searchLineEdit = QLineEdit()
        self.edit_search_line_placeholder()
        self.searchLineEdit.setObjectName("search")
        self.searchLineEdit.setClearButtonEnabled(True)

        # Add a button to add a new volunteer
        self.addVolunteerButton = QPushButton()
        self.addVolunteerButton.setObjectName("add")
        self.addVolunteerButton.setIcon(QIcon("images/addBlack.png"))
        self.addVolunteerButton.clicked.connect(lambda: self.emit_add())

        # Create a horizontal layout for search and add button
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchTypeComboBox)
        searchLayout.addWidget(self.searchLineEdit)
        searchLayout.addWidget(self.addVolunteerButton)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(searchLayout)

        # Main list widget to display volunteers
        self.volunteerList = QListWidget()
        mainLayout.addWidget(self.volunteerList)
        self.setLayout(mainLayout)

        # Preloader
        self.preloader = QMovie("images/volunteers.gif")
        self.preloaderLabel = QLabel()
        self.preloaderLabel.setMovie(self.preloader)
        self.preloaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.preloaderLabel)
        self.preloaderLabel.hide()

        # Connect search input and combo box to the search function
        self.searchLineEdit.textChanged.connect(self.perform_search)
        self.searchTypeComboBox.currentTextChanged.connect(
            lambda: self.edit_search_line_placeholder()
        )

        # set notifcation label
        self.notificationLabel = QLabel()
        self.notificationLabel.setObjectName("notification")
        mainLayout.addWidget(self.notificationLabel)
        self.notificationLabel.hide()

    def show_preloader(self):
        self.preloaderLabel.show()
        self.preloader.start()
        self.volunteerList.hide()

    def hide_preloader(self):
        self.preloaderLabel.hide()
        self.preloader.stop()
        self.volunteerList.show()

    def show_notification(self, message):
        self.notificationLabel.setText(message)
        self.notificationLabel.show()
        QTimer.singleShot(5000, lambda: self.notificationLabel.hide())

    def add_volunteer_to_list(self, volunteer: Volunteer, image: QPixmap):
        # Create a custom widget to hold volunteer information
        item_widget = QWidget()
        main_layout = QHBoxLayout(item_widget)

        # Left layout for image and details
        left_layout = QHBoxLayout()
        left_layout.setSpacing(2)

        image = image.scaled(
            50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation
        )
        rounded_image = QPixmap(image.size())
        rounded_image.fill(Qt.transparent)

        # Draw the circular mask
        painter = QPainter(rounded_image)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, image.width(), image.height())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, image)
        painter.end()

        # Set the rounded image to the QLabel
        image_label = QLabel()
        image_label.setPixmap(rounded_image)
        left_layout.addWidget(image_label)

        # Volunteer details label
        details = (
            f"ID: {volunteer.uniqueIdNumber}\n"
            f"{volunteer.firstName} {volunteer.lastName}\n"
            f"{volunteer.street} {volunteer.houseNumber} {volunteer.city}\n"
            f"{volunteer.phone}"
        )
        details_label = QLabel(details)
        details_label.setAlignment(Qt.AlignLeft)
        left_layout.addWidget(details_label)

        # Add left layout to main layout
        main_layout.addLayout(left_layout)

        # Buttons layout on the right
        right_layout = QHBoxLayout()
        right_layout.setAlignment(Qt.AlignRight)

        # Remove button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.emit_remove(volunteer))
        remove_button.setObjectName("remove")
        right_layout.addWidget(remove_button)

        # Update button
        update_button = QPushButton("Update")
        update_button.clicked.connect(lambda: self.emit_update(volunteer))
        update_button.setObjectName("update")
        right_layout.addWidget(update_button)

        # Add the right layout with buttons to the main layout
        main_layout.addLayout(right_layout)

        # Create a QListWidgetItem and set the custom widget
        list_item = QListWidgetItem(self.volunteerList)
        list_item.setSizeHint(item_widget.sizeHint())
        self.volunteerList.addItem(list_item)
        self.volunteerList.setItemWidget(list_item, item_widget)

    def set_volunteers(self, volunteers : List[ListVolunteer]):
        self.volunteers = volunteers
        self.volunteerList.clear()
        for listVolunteer in volunteers:
            self.add_volunteer_to_list(listVolunteer.volunteer, listVolunteer.img)

    def perform_search(self):
        search_term = self.searchLineEdit.text().strip()
        search_type = self.searchTypeComboBox.currentText()

        # Clear the volunteer list display before updating it
        self.volunteerList.clear()

        # Filter based on search type
        if search_type == "ID":
            filtered_volunteers = [
                v for v in self.volunteers if search_term in v.volunteer.uniqueIdNumber
            ]
        elif search_type == "Address":
            filtered_volunteers = [
                v
                for v in self.volunteers
                if search_term in f"{v.volunteer.street} {v.volunteer.houseNumber} {v.volunteer.city}"
            ]
        elif search_type == "Name":
            filtered_volunteers = [
                v
                for v in self.volunteers
                if search_term.lower() in v.volunteer.firstName.lower()
                or search_term.lower() in v.volunteer.lastName.lower()
            ]
        else:
            filtered_volunteers = self.volunteers

        # Display filtered volunteers
        for volunteer in filtered_volunteers:
            self.add_volunteer_to_list(volunteer.volunteer, volunteer.img)

    def edit_search_line_placeholder(self):
        self.searchLineEdit.clear()
        search_type = self.searchTypeComboBox.currentText()
        if search_type == "ID":
            self.searchLineEdit.setPlaceholderText("ID")
        elif search_type == "Address":
            self.searchLineEdit.setPlaceholderText("street, house number, city")
        elif search_type == "Name":
            self.searchLineEdit.setPlaceholderText("Name")
        else:
            self.searchLineEdit.setPlaceholderText("Search")

    def emit_remove(self, volunteer):
        self.removeVolunteerSignal.emit(volunteer)

    def emit_update(self, volunteer):
        self.updateVolunteerSignal.emit(volunteer)
        self.updateVolunteerClicked.emit()

    def emit_add(self):
        self.addVolunteerClicked.emit()
    
    def add_volunteer(self, volunteers: List[ListVolunteer]):
        self.show_notification("Volunteer added successfully")
        self.set_volunteers(volunteers)        
    
    def delete_volunteer(self, volunteers : List[ListVolunteer]):
        self.show_notification("Volunteer deleted successfully")
        self.set_volunteers(volunteers)
        
    def update_volunteer(self, volunteers: List[ListVolunteer]):
        self.show_notification("Volunteer updated successfully")
        self.set_volunteers(volunteers)

    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()
