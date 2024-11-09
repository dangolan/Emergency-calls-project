from models.mapModel import mapModel  # Import the corrected module and class


class MapController:
    def __init__(self, mapView):
        self.map_model = mapModel()  # Create an instance of MapModel
        self.mapView = mapView
        self.create_map()

    def create_map(self, eventLat=32.0853, eventLon=34.7818):
        volunteerRoute = self.map_model.get_volunteers_route(eventLat, eventLon)
        self.mapView.draw_map(volunteerRoute, eventLat, eventLon)
