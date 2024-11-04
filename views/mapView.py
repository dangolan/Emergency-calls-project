import sys
import io
import folium
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import requests
import random


class MapView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tel Aviv to Netanya Route")
        self.setGeometry(100, 100, 800, 700)  # Increased height for info label
        
        eventLat = 32.0853
        eventLon = 34.7818


        # Create a layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Create QWebEngineView
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        #fath the volunteers data
        volunteers = requests.get(f"http://localhost:7008/api/EventVolunteers/closestVolunteers?eventLat={eventLat}&eventLon={eventLon}").json()
        print("Volunteers data:", volunteers) 

        # Create the map
        self.create_map(volunteers, eventLat, eventLon)


    def create_map(self, volunteers, eventLat, eventLon):
        # Center the map between the event and volunteers
        if volunteers:
            # Calculate the center latitude and longitude
            center_lat = (eventLat + sum(volunteer['routeCoordinates'][0][1] for volunteer in volunteers)) / (1 + len(volunteers))
            center_lon = (eventLon + sum(volunteer['routeCoordinates'][0][0] for volunteer in volunteers)) / (1 + len(volunteers))
        else:
            # If there are no volunteers, center on the event location
            center_lat = eventLon
            center_lon = eventLon

        # Create the map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=15)


        # Add a marker for the event point in red
        folium.Marker(
            location=[eventLat, eventLon],
            popup="Event",
            icon=folium.Icon(color='red')
        ).add_to(m)

        # Draw routes for each volunteer in a different color and add markers for each volunteer
        for volunteer in volunteers:
            # Random color for each route
            route_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            
            # Extract the volunteer's coordinates
            coordinates = volunteer['routeCoordinates']
            
            # Draw the route on the map
            folium.PolyLine(
                locations=[coord[::-1] for coord in coordinates],  # Reverse coordinates for folium (lat, lon)
                weight=5,
                color=route_color,
                opacity=0.6
            ).add_to(m)

            # Add a blue marker for the volunteer's starting location
            folium.Marker(
                location=coordinates[0][::-1],  # Starting point of the route
                popup=f"Volunteer ID: {volunteer['volunteerId']}",
                icon=folium.Icon(color='blue')
            ).add_to(m)

        # Save the map to an HTML string
        data = io.BytesIO()
        m.save(data, close_file=False)
        map_html = data.getvalue().decode()

        # Set the HTML content to the QWebEngineView
        self.web_view.setHtml(map_html)

    def closeEvent(self, event):
        self.client.close()
        super().closeEvent(event)


