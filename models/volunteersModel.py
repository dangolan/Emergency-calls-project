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
            # fach img to pixmap object
            response = requests.get(volunteer.imageUrl)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                image = pixmap
            volunteers.append((volunteer, image))
        return volunteers

    def addVolunteer(self, volunteer):
        """Save the volunteer to the database or remote service."""
        url = "http://localhost:7008/api/Volunteers/Add"
        payload = {
            "id": volunteer.id,
            "uniqueIdNumber": volunteer.uniqueIdNumber,
            "firstName": volunteer.firstName,
            "lastName": volunteer.lastName,
            "phone": volunteer.phone,
            "latitude": volunteer.geoPoint.latitude,
            "longitude": volunteer.geoPoint.longitude,
            "city": volunteer.city,
            "street": volunteer.street,
            "houseNumber": volunteer.houseNumber,
            "imageUrl": volunteer.imageUrl,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:  # Assuming 201 indicates success
            return response.json().get("id", 0)
        else:
            raise Exception(
                f"Failed to save volunteer: {response.status_code} - {response.text}"
            )

    def update_volunteer(self, volunteer):
        url = "http://localhost:7008/api/Volunteers/Update/{volunteer.id}"
        response = requests.get(url)
        if response.status_code == 204:
            print(f"Updated volunteer with ID: {volunteer.id} successfully.")
            return volunteer.id
        else:
            raise Exception(
                f"Failed to update volunteer. Status code: {response.status_code} - {response.text}"
            )

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
