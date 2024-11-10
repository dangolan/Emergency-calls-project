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
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

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
        self.web_view.hide()
        self.spinner.start()  # Start the animation

    def hide_preloader(self):
        self.spinner.stop()  # Stop the animation
        self.web_view.show()
        self.preloader.setVisible(False)

    def draw_map(self, volunteers, eventLat, eventLon):
        
        # Create the map
        m = folium.Map(location=[eventLat, eventLon], zoom_start=12)

        # Add a marker for the event point in red
        folium.Marker(
            location=[eventLat, eventLon],
            popup="Event",
            icon=folium.Icon(color='red')
        ).add_to(m)

        if not volunteers:
            print("No volunteers to display on the map")
            # Save the map to an HTML string and display it
            data = io.BytesIO()
            m.save(data, close_file=False)
            map_html = data.getvalue().decode()
            self.web_view.setHtml(map_html)
            return

        # Draw routes for each volunteer in a different color and add markers for each volunteer
        for volunteer in volunteers:
            # Random color for each route
            route_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            
            # Extract the volunteer's coordinates
            coordinates = volunteer.get('routeCoordinates', [])
            if not coordinates:
                print(f"Warning: No route coordinates for volunteer {volunteer.get('volunteerId')}")
                continue
            
            # Draw the route on the map
            folium.PolyLine(
                locations=[coord[::-1] for coord in coordinates],  # Reverse coordinates for folium (lat, lon)
                weight=5,
                color=route_color,
                opacity=0.6
            ).add_to(m)
            

           # Assuming 'coordinates' and 'volunteer' are already defined
            full_name = f"{volunteer['volunteer']['firstName']} {volunteer['volunteer']['lastName']}"
            photo_url = volunteer['volunteer']['photoUrl']
            # HTML content for the custom icon (image inside a circular background)
            html = f"""
                <div style="background-color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">
                    <img src="{photo_url}" style="border-radius: 50%; width: 28px; height: 28px;">
                </div>
            """
            icon = folium.DivIcon(html=html)

            # Add the custom marker with the volunteer's photo and name in the popup
            folium.Marker(
                location=[coordinates[0][1], coordinates[0][0]],  # Starting point of the route
                popup=full_name,  # Display the name in the popup
                icon=icon  # Custom icon with the volunteer's image
            ).add_to(m)


        # Save the map to an HTML string and display it
        data = io.BytesIO()
        m.save(data, close_file=False)
        map_html = data.getvalue().decode()

        # Set the HTML content to the QWebEngineView
        self.web_view.setHtml(map_html)