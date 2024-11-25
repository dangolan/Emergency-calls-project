
from entities.volunteer import Volunteer
from PySide6.QtGui import QPixmap

class ListVolunteer:
    def __init__(self, volunteer: Volunteer, img: QPixmap):
        self.volunteer = volunteer
        self.img = img