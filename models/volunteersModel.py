class VolunteersModel():
    def __init__(self):
        self.volunteers = []

    def add_volunteer(self, volunteer):
        self.volunteers.append(volunteer)

    def get_volunteers(self):
        return self.volunteers
    def get_volunteer(self, id):
        for volunteer in self.volunteers:
            if volunteer.id == id:
                return volunteer
        return None
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
