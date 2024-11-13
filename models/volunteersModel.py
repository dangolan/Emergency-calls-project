import requests
from entities.volunteer import Volunteer


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
            volunteers.append(volunteer)
        return volunteers

    def add_volunteer(self, volunteer):
        self.volunteers.append(volunteer)

    def update_volunteer(self, id, volunteer):
        for i in range(len(self.volunteers)):
            if self.volunteers[i].id == id:
                self.volunteers[i] = volunteer
                return True
        return False

    def delete_volunteer(self, id):
        for i in range(len(self.volunteers)):
            if self.volunteers[i].id == id:
                del self.volunteers[i]
                return True
        return False
