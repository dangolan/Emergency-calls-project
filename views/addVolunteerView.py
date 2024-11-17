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


class AddVolunteerView(QWidget):
    def __init__(self,volunteer: Volunteer = None):
        super().__init__()

        self.setWindowTitle("Add Volunteer")
        self.setAcceptDrops(True)  # Enable drag-and-drop

        # Main layout
        mainLayout = QVBoxLayout(self)

        # Form layout
        formLayout = QFormLayout()
        #header label
        headerLabel = QLabel("Add Volunteer")
        if volunteer:
            headerLabel.setText("Edit Volunteer")
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
        #set placeholder text
        self.uniqueIdNumberField.setPlaceholderText("ID number")
        self.firstNameField.setPlaceholderText("First name")
        self.lastNameField.setPlaceholderText("Last name")
        self.phoneField.setPlaceholderText("Phone number")
        self.city.setPlaceholderText("City")
        self.street.setPlaceholderText("Street")
        self.houseNumber.setPlaceholderText("House number")

        if volunteer:
            self.uniqueIdNumberField.setText(volunteer.uniqueIdNumber)
            self.firstNameField.setText(volunteer.firstName)
            self.lastNameField.setText(volunteer.lastName)
            self.phoneField.setText(volunteer.phone)
            self.city.setText(volunteer.city)
            self.street.setText(volunteer.street)
            self.houseNumber.setText(volunteer.houseNumber)
        #add qhbox layout for first name and last name
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(self.firstNameField)
        nameLayout.addWidget(self.lastNameField)

        #add qhbox layout for city, street and house number
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
        saveButton = QPushButton("Save")
        saveButton.setObjectName("save")
        cancelButton = QPushButton("Cancel")
        cancelButton.setObjectName("cancel")
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)

        # Add buttons to main layout
        mainLayout.addLayout(buttonLayout)

        #set style sheet
        self.setStyleSheet(self.loadStyleSheet("views/styles/addVolunteer.qss"))

        # Connect buttons to actions
        saveButton.clicked.connect(self.saveVolunteer)
        cancelButton.clicked.connect(self.close)

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
        """Save volunteer information."""
        volunteerID = self.volunteer.id if self.volunteer else 0
        # Collect data from the fields
        volunteer = Volunteer(
            volunteerID,
            self.uniqueIdNumberField.text(),
            self.firstNameField.text(),
            self.lastNameField.text(),
            self.phoneField.text(),
            self.city.text(),
            self.street.text(),
            self.houseNumber.text(),
            ""
        )
        # Handle saving logic here
        self.close()
    def loadStyleSheet(self, name):
        with open(name, "r") as file:
            return file.read()
