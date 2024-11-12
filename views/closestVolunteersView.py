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
from PySide6.QtGui import QPainter, QColor, QBrush, QMovie


class ClosestVolunteersView(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main vertical layout
        main_layout = QVBoxLayout(self)        

        # Create a QListWidget to hold the list of volunteers
        self.listWidget = QListWidget()

        # Store items in a separate list for filtering
        self.itemsData = []

        # Add the list widget to the layout
        main_layout.addWidget(self.listWidget)

        self.setLayout(main_layout)
        self.resize(400, 500)

        #set preloader
        self.preloader = QMovie("images/volunteers.gif")
        self.preloaderLabel = QLabel()
        self.preloaderLabel.setMovie(self.preloader)
        self.preloaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.preloaderLabel)
        self.preloaderLabel.hide()


        stylesheet = self.load_stylesheet("views/styles/closestVolunteers.qss")
        self.setStyleSheet(stylesheet)

    def show_preloader(self):
        self.preloaderLabel.show()
        self.preloader.start()
        self.listWidget.hide()

    def hide_preloader(self):
        self.preloaderLabel.hide()
        self.preloader.stop()
        self.listWidget.show()

    
    def add_volunteers(self, eventVolunteers):
        self.itemsData.clear()  # Reset the items data list

        # Sort event volunteers by duration
        sortedEventVolunteers = sorted(eventVolunteers, key=lambda ev: ev.duration)

        for eventVolunteer in sortedEventVolunteers:
            volunteer = eventVolunteer.volunteer
            distanceKm = eventVolunteer.distance / 1000  # Convert to kilometers
            durationMinutes = eventVolunteer.duration / 60  # Convert to minutes

            # Create a widget for each volunteer
            volunteerWidget = QWidget()
            volunteerLayout = QHBoxLayout()
            volunteerLayout.setSpacing(10)

            # Load volunteer image
            photoUrl = volunteer.imageUrl
            try:
                response = requests.get(photoUrl)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(BytesIO(response.content).read())

                    # Create a circular image
                    roundedPixmap = QPixmap(pixmap.size())
                    roundedPixmap.fill(QColor("transparent"))
                    painter = QPainter(roundedPixmap)
                    painter.setRenderHint(QPainter.Antialiasing)
                    painter.setBrush(QBrush(pixmap))
                    painter.setPen(Qt.transparent)
                    painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
                    painter.end()

                    # Set the rounded image
                    photoLabel = QLabel()
                    photoLabel.setPixmap(roundedPixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    photoLabel.setObjectName("photoLabel")
                else:
                    photoLabel = QLabel("No Image")
            except Exception as e:
                photoLabel = QLabel("Image Load Error")

            # Add photo to layout (right side)
            volunteerLayout.addWidget(photoLabel)

            # Volunteer details (left side)
            details = f"{volunteer.firstName} {volunteer.lastName}\n" \
                    f"{volunteer.city} {volunteer.street} {volunteer.houseNumber}\n" \
                    f"Distance: {distanceKm:.2f} km\n" \
                    f"Duration: {durationMinutes:.2f} min"
            detailsLabel = QLabel(details)
            detailsLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            # Add details to layout
            volunteerLayout.addWidget(detailsLabel)

            # Set the layout for the volunteer widget
            volunteerWidget.setLayout(volunteerLayout)

            # Create a QListWidgetItem and set its custom widget
            listItem = QListWidgetItem()
            listItem.setSizeHint(volunteerWidget.sizeHint())  # Set the size of the item to match the widget
            self.listWidget.addItem(listItem)  # Add item to the list
            self.listWidget.setItemWidget(listItem, volunteerWidget)  # Set the widget for the list item

            # Store the volunteer's text and details for filtering
            self.itemsData.append((f"{volunteer.firstName} {volunteer.lastName}", details))


    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()
    def clear(self):
        self.listWidget.clear()
