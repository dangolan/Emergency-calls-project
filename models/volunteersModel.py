from mimetypes import guess_type
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

    def addVolunteer(self, volunteer: Volunteer):
        print(
            "Adding volunteer:",
            volunteer.id,
            volunteer.firstName,
            volunteer.lastName,
            volunteer.imageUrl,
            volunteer.geoPoint.latitude,
            volunteer.geoPoint.longitude,
            volunteer.phone,
            volunteer.city,
            volunteer.street,
            volunteer.houseNumber,
        )
        url = "http://localhost:7008/api/Volunteers/Add"

        # Prepare the volunteer data as a dictionary
        volunteer_data = {
            "Id": volunteer.id,
            "UniqueIdNumber": volunteer.uniqueIdNumber,
            "FirstName": volunteer.firstName,
            "LastName": volunteer.lastName,
            "Phone": volunteer.phone,
            "Country": "ישראל",
            "City": volunteer.city,
            "Street": volunteer.street,
            "HouseNumber": volunteer.houseNumber,
            "PhotoUrl": volunteer.imageUrl,
            "Latitude": volunteer.geoPoint.latitude,
            "Longitude": volunteer.geoPoint.longitude,
        }

        # Prepare the photo file if provided
        files = (
            {"Photo": open(volunteer.imageUrl, "rb")} if volunteer.imageUrl else None
        )

        try:
            # Send the POST request with form-data
            response = requests.post(url, data=volunteer_data, files=files)

            # Handle the response
            if response.status_code == 201:
                print("Volunteer added successfully:", response.json())
            else:
                print(
                    f"Failed to add volunteer: {response.status_code}, {response.text}"
                )

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the file if it was opened
            if files:
                files["Photo"].close()

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
