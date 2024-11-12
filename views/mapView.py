import sys
import io
import base64
import folium
import requests
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import random
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QLabel
from folium.features import CustomIcon


class MapView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tel Aviv to Netanya Route")
        self.setGeometry(100, 100, 800, 700)  # Increased height for info label

        # Create a layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Create QWebEngineView
        self.webView = QWebEngineView()
        self.layout.addWidget(self.webView)

         # Create a QLabel for the preloading spinner
        self.preloader = QLabel(self)
        self.layout.addWidget(self.preloader)
        self.preloader.setAlignment(Qt.AlignCenter)

        # Set the spinner GIF
        self.spinner = QMovie("images/spinner.gif")  # Replace with your actual spinner path
        self.preloader.setMovie(self.spinner)

        # Initially hide the spinner
        self.preloader.setVisible(False)

    def show_preloader(self):
        self.preloader.setVisible(True)
        self.webView.hide()
        self.spinner.start()  # Start the animation

    def hide_preloader(self):
        self.spinner.stop()  # Stop the animation
        self.webView.show()
        self.preloader.setVisible(False)



    def draw_map(self, eventVolunteers, eventLat, eventLon):
        # Create the map
        m = folium.Map(location=[eventLat, eventLon], zoom_start=12)

        # Add a marker for the event point in red
        folium.Marker(
            location=[eventLat, eventLon],
            popup="Event",
            icon=folium.Icon(color='red')
        ).add_to(m)

        if not eventVolunteers:
            print("No volunteers to display on the map")
            # Save the map to an HTML string and display it
            data = io.BytesIO()
            m.save(data, close_file=False)
            mapHtml = data.getvalue().decode()
            self.webView.setHtml(mapHtml)
            return

        # Draw routes for each volunteer in a different color and add markers for each volunteer
        for eventVolunteer in eventVolunteers:
            # Random color for each route
            routeColor = "#{:06x}".format(random.randint(0, 0xFFFFFF))

            # Extract route coordinates
            coordinates = eventVolunteer.routeCoordinates
            if not coordinates:
                print(f"Warning: No route coordinates for volunteer {eventVolunteer.volunteer.id}")
                continue

            # Draw the route on the map
            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in coordinates],  # Reverse coordinates for folium (lat, lon)
                weight=5,
                color=routeColor,
                opacity=0.6
            ).add_to(m)

            # Extract volunteer details
            volunteer = eventVolunteer.volunteer
            fullName = f"{volunteer.firstName} {volunteer.lastName}"
            photoUrl = volunteer.imageUrl

            # HTML content for the custom icon (image inside a circular background)
            html = f"""
                <div style="background-color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">
                    <img src="{photoUrl}" style="border-radius: 50%; width: 28px; height: 28px;">
                </div>
            """
            icon = folium.DivIcon(html=html)

            # Add the custom marker with the volunteer's photo and name in the popup
            folium.Marker(
                location=[coordinates[0][1], coordinates[0][0]],  # Starting point of the route
                popup=fullName,  # Display the name in the popup
                icon=icon  # Custom icon with the volunteer's image
            ).add_to(m)

        # Save the map to an HTML string and display it
        data = io.BytesIO()
        m.save(data, close_file=False)
        mapHtml = data.getvalue().decode()
        self.webView.setHtml(mapHtml)


        # Set the HTML content to the QWebEngineView
        self.webView.setHtml(mapHtml)