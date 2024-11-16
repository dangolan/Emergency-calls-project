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


class AddVolunteerView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Volunteer")
        self.setAcceptDrops(True)  # Enable drag-and-drop

        # Main layout
        mainLayout = QVBoxLayout(self)

        # Form layout
        formLayout = QFormLayout()

        # Add form fields
        self.idField = QLineEdit()
        self.uniqueIdNumberField = QLineEdit()
        self.firstNameField = QLineEdit()
        self.lastNameField = QLineEdit()
        self.phoneField = QLineEdit()
        self.addressField = QLineEdit()

        # Add form fields to layout
        formLayout.addRow("ID:", self.idField)
        formLayout.addRow("Unique ID Number:", self.uniqueIdNumberField)
        formLayout.addRow("First Name:", self.firstNameField)
        formLayout.addRow("Last Name:", self.lastNameField)
        formLayout.addRow("Phone:", self.phoneField)
        formLayout.addRow("Address:", self.addressField)

        # Image field with drag-and-drop
        self.imageLabel = QLabel("Drag and drop an image here")
        self.imageLabel.setStyleSheet("border: 2px dashed #aaaaaa; padding: 2px;")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFixedHeight(100)
        formLayout.addRow("Image:", self.imageLabel)

        # Add the form layout to the main layout
        mainLayout.addLayout(formLayout)

        # Buttons
        buttonLayout = QHBoxLayout()
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)

        # Add buttons to main layout
        mainLayout.addLayout(buttonLayout)

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
        # Collect data from the fields
        data = {
            "id": self.idField.text(),
            "uniqueIdNumber": self.uniqueIdNumberField.text(),
            "firstName": self.firstNameField.text(),
            "lastName": self.lastNameField.text(),
            "phone": self.phoneField.text(),
            "address": self.addressField.text(),
            "imageUrl": self.imageLabel.toolTip(),  # The image path
        }
        QMessageBox.information(
            self, "Volunteer Saved", f"Volunteer information saved:\n{data}"
        )
        # Handle saving logic here
        self.close()
