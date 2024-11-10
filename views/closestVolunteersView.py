from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import requests
from io import BytesIO
from PySide6.QtGui import QPainter, QColor, QBrush


class ClosestVolunteersView(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main vertical layout
        main_layout = QVBoxLayout(self)        

        # Create a QListWidget to hold the list of volunteers
        self.list_widget = QListWidget()

        # Store items in a separate list for filtering
        self.items_data = []

        # Add the list widget to the layout
        main_layout.addWidget(self.list_widget)

        self.setLayout(main_layout)
        self.resize(400, 500)

        stylesheet = self.load_stylesheet("views/styles/closestVolunteers.qss")
        self.setStyleSheet(stylesheet)

    
    def add_volunteers(self, volunteers):
        self.items_data.clear()  # Reset the items data list
        # Sort volunteers by duration
        sorted_volunteers = sorted(volunteers, key=lambda v: v["duration"])

        for volunteer_data in sorted_volunteers:
            volunteer = volunteer_data["volunteer"]
            distance = volunteer_data["distance"]
            duration = volunteer_data["duration"]

            # Convert duration to minutes and distance to kilometers
            duration_minutes = duration / 60
            distance_km = distance / 1000

            # Create a widget for each volunteer
            volunteer_widget = QWidget()
            volunteer_layout = QHBoxLayout()
            volunteer_layout.setSpacing(10)

            # Load volunteer image
            photo_url = volunteer["photoUrl"]
            try:
                response = requests.get(photo_url)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(BytesIO(response.content).read())

                    # Create a circular image
                    rounded_pixmap = QPixmap(pixmap.size())
                    rounded_pixmap.fill(QColor("transparent"))
                    painter = QPainter(rounded_pixmap)
                    painter.setRenderHint(QPainter.Antialiasing)
                    painter.setBrush(QBrush(pixmap))
                    painter.setPen(Qt.transparent)
                    painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
                    painter.end()

                    # Set the rounded image
                    photo_label = QLabel()
                    photo_label.setPixmap(rounded_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    photo_label.setObjectName("photoLabel")
                else:
                    photo_label = QLabel("No Image")
            except Exception as e:
                photo_label = QLabel("Image Load Error")

            # Add photo to layout (right side)
            volunteer_layout.addWidget(photo_label)

            # Volunteer details (left side)
            details = f"{volunteer['firstName']} {volunteer['lastName']}\n" \
                    f"{volunteer['city']} {volunteer['street']} {volunteer['houseNumber']}\n" \
                    f"Distance: {distance_km:.2f} km\n" \
                    f"Duration: {duration_minutes:.2f} min"
            details_label = QLabel(details)
            details_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            # Add details to layout
            volunteer_layout.addWidget(details_label)

            # Set the layout for the volunteer widget
            volunteer_widget.setLayout(volunteer_layout)

            # Create a QListWidgetItem and set its custom widget
            list_item = QListWidgetItem()
            list_item.setSizeHint(volunteer_widget.sizeHint())  # Set the size of the item to match the widget
            self.list_widget.addItem(list_item)  # Add item to the list
            self.list_widget.setItemWidget(list_item, volunteer_widget)  # Set the widget for the list item

            # Store the volunteer's text and details for filtering
            self.items_data.append((f"{volunteer['firstName']} {volunteer['lastName']}", details))

    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()
    def clear(self):
        self.list_widget.clear()
