import requests
from entities.volunteer import Volunteer
from io import BytesIO
from PySide6.QtGui import QPixmap


class VolunteersModel:
    def __init__(self):
        pass

    def get_all_volunteers(self):
        url = "http://localhost:7008/api/Volunteers/GetAll"
        response = requests.get(url)
        if response.status_code == 200:
            response_data = response.json()
            print(
                f"Fetched {len(response_data)} volunteers from server."
            )  # Add this line
            return self.parse_response_to_volunteers(response_data)
        else:
            print(f"Failed to get volunteers. Status code: {response.status_code}")
            raise Exception(
                f"Failed to get volunteers. Status code: {response.status_code} - {response.text}"
            )

    def parse_response_to_volunteers(self, response_data):
        volunteers = []
        for item in response_data:
            volunteer = Volunteer(
                id=item["id"],
                uniqueIdNumber=item["uniqueIdNumber"],
                firstName=item["firstName"],
                lastName=item["lastName"],
                phone=item["phone"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                city=item["city"],
                street=item["street"],
                houseNumber=item["houseNumber"],
                imageUrl=item["photoUrl"],
            )
            #fach img to pixmap object
            response = requests.get(volunteer.imageUrl)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                image = pixmap
            volunteers.append((volunteer, image))
        return volunteers

    def add_volunteer(self, volunteer):
        self.volunteers.append(volunteer)

    def update_volunteer(self, id, volunteer):
        for i in range(len(self.volunteers)):
            if self.volunteers[i].id == id:
                self.volunteers[i] = volunteer
                return True
        return False

    def delete_volunteer(self, volunteer):
        url = f"http://localhost:7008/api/Volunteers/Delete/{volunteer.id}"
        response = requests.delete(url)
        if response.status_code == 204:
            print(f"Deleted volunteer with ID: {volunteer.id} successfully.")
            return volunteer.id
        else:
            raise Exception(
                f"Failed to delete volunteer. Status code: {response.status_code} - {response.text}"
            )