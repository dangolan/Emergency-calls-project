import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from entities.volunteer import Volunteer
from PySide6.QtCore import Signal
from entities.volunteer import GeoPoint  # Import GeoPoint


class AddVolunteerView(QWidget):
    save_volunteer_signal = Signal(Volunteer)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Volunteer")
        self.setAcceptDrops(True)  # Enable drag-and-drop
        # Main layout
        mainLayout = QVBoxLayout(self)
        # Form layout
        formLayout = QFormLayout()
        # header label
        headerLabel = QLabel("Add Volunteer")
        # set the label to center
        headerLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(headerLabel)
        # Add form fields
        self.uniqueIdNumberField = QLineEdit()
        self.firstNameField = QLineEdit()
        self.lastNameField = QLineEdit()
        self.phoneField = QLineEdit()
        self.city = QLineEdit()
        self.street = QLineEdit()
        self.houseNumber = QLineEdit()
        # set placeholder text
        self.uniqueIdNumberField.setPlaceholderText("ID number")
        self.firstNameField.setPlaceholderText("First name")
        self.lastNameField.setPlaceholderText("Last name")
        self.phoneField.setPlaceholderText("Phone number")
        self.city.setPlaceholderText("City")
        self.street.setPlaceholderText("Street")
        self.houseNumber.setPlaceholderText("House number")

        # add qhbox layout for first name and last name
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(self.firstNameField)
        nameLayout.addWidget(self.lastNameField)

        # add qhbox layout for city, street and house number
        addressLayout = QHBoxLayout()
        addressLayout.addWidget(self.city)
        addressLayout.addWidget(self.street)
        addressLayout.addWidget(self.houseNumber)
        # Add form fields to the form layout
        formLayout.addRow(self.uniqueIdNumberField)
        formLayout.addRow(nameLayout)
        formLayout.addRow(self.phoneField)
        formLayout.addRow(addressLayout)

        # Image field with drag-and-drop
        self.imageLabel = QLabel("Drag and drop an image here")
        self.imageLabel.setStyleSheet("border: 2px dashed #aaaaaa; padding: 2px;")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFixedHeight(100)
        formLayout.addRow(self.imageLabel)

        # Add the form layout to the main layout
        mainLayout.addLayout(formLayout)
        # Buttons
        buttonLayout = QHBoxLayout()

        cancelButton = QPushButton("Cancel")
        cancelButton.setObjectName("cancel")
        buttonLayout.addWidget(cancelButton)
        cancelButton.clicked.connect(self.close)

        saveButton = QPushButton("Save")
        saveButton.setObjectName("save")
        buttonLayout.addWidget(saveButton)
        mainLayout.addLayout(buttonLayout)
        saveButton.clicked.connect(self.saveVolunteer)

        # set style sheet
        self.setStyleSheet(self.loadStyleSheet("views/styles/addVolunteer.qss"))

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith((".png")):
                pixmap = QPixmap(file_path)
                self.imageLabel.setPixmap(
                    pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio)
                )
                self.imageLabel.setToolTip(file_path)  # Save file path in the tooltip
            else:
                QMessageBox.warning(
                    self, "Invalid File", "Please drop a valid image file."
                )

    def saveVolunteer(self):
        volunteerID = 0
        image_path = self.imageLabel.toolTip() or ""

        # Collect data and validate
        if not self.uniqueIdNumberField.text().strip():
            QMessageBox.warning(self, "Validation Error", "ID number cannot be empty.")
            return

        if (
            not self.firstNameField.text().strip()
            or not self.lastNameField.text().strip()
        ):
            QMessageBox.warning(
                self, "Validation Error", "First and last name cannot be empty."
            )
            return

        volunteer = Volunteer(
            volunteerID,
            uniqueIdNumber=self.uniqueIdNumberField.text(),
            firstName=self.firstNameField.text(),
            lastName=self.lastNameField.text(),
            phone=self.phoneField.text(),
            city=self.city.text(),
            street=self.street.text(),
            houseNumber=self.houseNumber.text(),
            imageUrl=image_path,
            latitude=0,
            longitude=0,
        )
        self.save_volunteer_signal.emit(volunteer)
        self.close()

    def set_volunteer(self, volunteer):
        self.uniqueIdNumberField.setText(volunteer.uniqueIdNumber)
        self.firstNameField.setText(volunteer.firstName)
        self.lastNameField.setText(volunteer.lastName)
        self.phoneField.setText(volunteer.phone)
        self.city.setText(volunteer.city)
        self.street.setText(volunteer.street)
        self.houseNumber.setText(volunteer.houseNumber)

        # Set the image
        if volunteer.imageUrl:
            pixmap = QPixmap()
            pixmap.loadFromData(volunteer.imageUrl)
            self.imageLabel.setPixmap(
                pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio)
            )
            self.imageLabel.setToolTip(volunteer.imageUrl)

    def loadStyleSheet(self, name):
        with open(name, "r") as file:
            return file.read()
