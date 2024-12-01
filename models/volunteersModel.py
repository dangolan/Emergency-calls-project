from mimetypes import guess_type
import requests
from entities.volunteer import Volunteer
from io import BytesIO
from PySide6.QtGui import QPixmap
from entities.listVolunteer import ListVolunteer
from typing import List


class VolunteersModel:
    # volunteers model
    def __init__(self):
        pass
        self.volunteers : List[ListVolunteer] = []

    # get all volunteers from server
    def get_all_volunteers(self):
        url = "http://localhost:7008/api/Volunteers/GetAll"
        response = requests.get(url)
        if response.status_code == 200:
            response_data = response.json()
            print(
                f"Fetched {len(response_data)} volunteers from server."
            )  # Add this line
            self.volunteers = self.parse_response_to_volunteers(response_data)
            return self.volunteers
        else:
            print(f"Failed to get volunteers. Status code: {response.status_code}")
            raise Exception(
                f"Failed to get volunteers. Status code: {response.status_code} - {response.text}"
            )

    # get volunteer by id
    def get_volunteer(self, id):
        url = f"http://localhost:7008/api/Volunteers/Get/{id}"
        response = requests.get(url)
        if response.status_code == 200:
            response_data = response.json()
            print(f"Fetched volunteer with ID: {id} from server.")
            return self.parse_to_volunteer(response_data)
        else:
            print(
                f"Failed to get volunteer with ID: {id}. Status code: {response.status_code}"
            )
            raise Exception(
                f"Failed to get volunteer with ID: {id}. Status code: {response.status_code} - {response.text}"
            )

    # add volunteer to server
    def add_volunteer(self, volunteer: Volunteer):
        url = "http://localhost:7008/api/Volunteers/Add"
        # Prepare the volunteer data as a dictionary
        volunteer_data = {
            "Id": 0,
            "UniqueIdNumber": volunteer.uniqueIdNumber,
            "FirstName": volunteer.firstName,
            "LastName": volunteer.lastName,
            "Phone": volunteer.phone,
            "Country": "ישראל",
            "City": volunteer.city,
            "Street": volunteer.street,
            "HouseNumber": volunteer.houseNumber,
            "PhotoUrl": "none",
            "Latitude": 0,
            "Longitude": 0,
        }

        files = None
        if volunteer.imageUrl:
            try:
                files = {
                    "Photo": ("photo.png", open(volunteer.imageUrl, "rb"), "image/png")
                }
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Error: The file at '{volunteer.imageUrl}' was not found."
                )
            finally:
                # Close the file if it was opened
                if "Photo" in files and hasattr(files["Photo"], "close"):
                    files["Photo"].close()
            # Send the POST request with form-data
            response = requests.post(url, data=volunteer_data, files=files)
            # Handle the response
            if response.status_code == 201:
                print("Volunteer added successfully:")
                newVolunteer = self.parse_to_volunteer(response.json())
                self.volunteers.append(newVolunteer)
                return self.volunteers
            else:
                raise Exception(
                    f"Failed to get volunteers. Status code: {response.status_code} - {response.text}"
                )

    # update volunteer
    def update_volunteer(self, volunteer):
        url = f"http://localhost:7008/api/Volunteers/Update/{volunteer.id}"
        volunteer_data = {
            "Id": 0,
            "UniqueIdNumber": volunteer.uniqueIdNumber,
            "FirstName": volunteer.firstName,
            "LastName": volunteer.lastName,
            "Phone": volunteer.phone,
            "Country": "ישראל",
            "City": volunteer.city,
            "Street": volunteer.street,
            "HouseNumber": volunteer.houseNumber,
            "PhotoUrl": "none",
            "Latitude": 0,
            "Longitude": 0,
        }
        if volunteer.imageUrl:
            try:
                files = {
                    "Photo": ("photo.png", open(volunteer.imageUrl, "rb"), "image/png")
                }
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Error: The file at '{volunteer.imageUrl}' was not found."
                )
            finally:
                # Close the file if it was opened
                if "Photo" in files and hasattr(files["Photo"], "close"):
                    files["Photo"].close()
            response = requests.put(url, data=volunteer_data, files=files)
        else:
            response = requests.put(url, data=volunteer_data)
        if response.status_code == 204:
            print(f"Updated volunteer with ID: {volunteer.id} successfully.")
            updateVolunteer = self.get_volunteer(volunteer.id)
            for i, v in enumerate(self.volunteers):
                if v.volunteer.id == volunteer.id:
                    self.volunteers[i] = updateVolunteer
            return self.volunteers
        else:
            raise Exception(
                f"Failed to update volunteer. Status code: {response.status_code} - {response.text}"
            )

    # delete volunteer
    def delete_volunteer(self, volunteer):
        url = f"http://localhost:7008/api/Volunteers/Delete/{volunteer.id}"
        response = requests.delete(url)
        if response.status_code == 204:
            print(f"Deleted volunteer with ID: {volunteer.id} successfully.")
            for i, v in enumerate(self.volunteers):
                if v.volunteer.id == volunteer.id:
                    self.volunteers.pop(i)
            return self.volunteers
        else:
            raise Exception(
                f"Failed to delete volunteer. Status code: {response.status_code} - {response.text}"
            )

    # parse response to volunteers
    def parse_response_to_volunteers(self, response_data):
        volunteers = []
        for item in response_data:
            volunteers.append(self.parse_to_volunteer(item))
        return volunteers

    # parse response to volunteer object
    def parse_to_volunteer(self, response_data):
        volunteer = Volunteer(
            id=response_data["id"],
            uniqueIdNumber=response_data["uniqueIdNumber"],
            firstName=response_data["firstName"],
            lastName=response_data["lastName"],
            phone=response_data["phone"],
            latitude=response_data["latitude"],
            longitude=response_data["longitude"],
            city=response_data["city"],
            street=response_data["street"],
            houseNumber=response_data["houseNumber"],
            imageUrl=response_data["photoUrl"],
        )
        imgResponse = requests.get(volunteer.imageUrl)
        if imgResponse.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(imgResponse.content).read())
            image = pixmap
        return ListVolunteer(volunteer, image)
