from PySide6.QtWidgets import (
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
import re


class AddVolunteerView(QWidget):
    saveVolunteerSignal = Signal(Volunteer)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Volunteer")
        self.setAcceptDrops(True)  # Enable drag-and-drop
        # Main layout
        mainLayout = QVBoxLayout(self)
        # Form layout
        formLayout = QFormLayout()

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
        cancelButton.clicked.connect(self.close_window)

        saveButton = QPushButton("Save")
        saveButton.setObjectName("save")
        buttonLayout.addWidget(saveButton)
        mainLayout.addLayout(buttonLayout)
        saveButton.clicked.connect(self.save_volunteer)
        # set volunter id
        self.volunteerID = 0

        # set style sheet
        self.setStyleSheet(self.loadStyleSheet("views/styles/addVolunteer.qss"))

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
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

    def remove_img(self):
        # Explicitly clear the pixmap
        self.imageLabel.setPixmap(QPixmap())
        # Clear any text and reset the label
        self.imageLabel.clear()
        self.imageLabel.setText("Drag and drop an image here")
        self.imageLabel.setStyleSheet("border: 2px dashed #aaaaaa; padding: 2px;")
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setFixedHeight(100)
        self.imageLabel.setToolTip("")  # Clear the tooltip

    def save_volunteer(self):
        image_path = self.imageLabel.toolTip() or ""

        # Retrieve input values
        uniqueIdNumber = self.uniqueIdNumberField.text().strip()
        firstName = self.firstNameField.text().strip()
        lastName = self.lastNameField.text().strip()
        phone = self.phoneField.text().strip()
        city = self.city.text().strip()
        street = self.street.text().strip()
        houseNumber = self.houseNumber.text().strip()

        # Input validation
        if not uniqueIdNumber.isdigit():
            QMessageBox.critical(
                self, "Invalid Input", "Unique ID Number must contain only digits."
            )
            return

        if not re.match("^[a-zA-Z]+$", firstName):
            QMessageBox.critical(
                self, "Invalid Input", "First Name must contain only English letters."
            )
            return

        if not re.match("^[a-zA-Z]+$", lastName):
            QMessageBox.critical(
                self, "Invalid Input", "Last Name must contain only English letters."
            )
            return

        if not phone.isdigit():
            QMessageBox.critical(
                self, "Invalid Input", "Phone number must contain only digits."
            )
            return

        if not re.match("^[א-ת\s]+$", city):
            QMessageBox.critical(
                self, "Invalid Input", "City must contain only Hebrew letters."
            )
            return

        if not re.match("^[א-ת\s]+$", street):
            QMessageBox.critical(
                self, "Invalid Input", "Street must contain only Hebrew letters."
            )
            return
        if not houseNumber.isdigit():
            QMessageBox.critical(
                self, "Invalid Input", "House number must contain only digits."
            )
            return
        if self.volunteerID == 0:
            if not image_path:
                QMessageBox.critical(self, "Invalid Input", "Please upload an image.")
                return

        # Create Volunteer instance
        volunteer = Volunteer(
            self.volunteerID,
            uniqueIdNumber=uniqueIdNumber,
            firstName=firstName,
            lastName=lastName,
            phone=phone,
            city=city,
            street=street,
            houseNumber=houseNumber,
            imageUrl=image_path,
            latitude=0,
            longitude=0,
        )

        # Emit signal and close the window
        self.saveVolunteerSignal.emit(volunteer)
        self.close_window()

    def close_window(self):
        self.uniqueIdNumberField.clear()
        self.firstNameField.clear()
        self.lastNameField.clear()
        self.phoneField.clear()
        self.city.clear()
        self.street.clear()
        self.houseNumber.clear()
        self.remove_img()
        self.volunteerID = 0
        self.close()

    def set_volunteer(self, volunteer):
        self.volunteerID = volunteer.id
        self.uniqueIdNumberField.setText(volunteer.uniqueIdNumber)
        self.firstNameField.setText(volunteer.firstName)
        self.lastNameField.setText(volunteer.lastName)
        self.phoneField.setText(volunteer.phone)
        self.city.setText(volunteer.city)
        self.street.setText(volunteer.street)
        self.houseNumber.setText(volunteer.houseNumber)

    def loadStyleSheet(self, name):
        with open(name, "r") as file:
            return file.read()
