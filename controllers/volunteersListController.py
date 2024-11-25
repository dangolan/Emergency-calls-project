from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from worker import Worker


class VolunteersListController(QObject):
    errorSignal = Signal(str)

    def __init__(
        self, volunteersListView=None, volunteersModel=None, addVolunteerView=None
    ):
        super().__init__()
        print("VolunteersListController")
        self.volunteersListView = volunteersListView
        self.addVolunteerView = addVolunteerView
        self.model = volunteersModel
        self.volunteersListView.removeVolunteerSignal.connect(self.remove_volunteer)
        self.volunteersListView.updateVolunteerSignal.connect(self.addVolunteerView.set_volunteer)
        self.addVolunteerView.saveVolunteerSignal.connect(self.add_update_volunteer)
        self.load_volunteer()

    def load_volunteer(self):
        # Call the async function and wait for the result
        self.volunteersListView.show_preloader()

        def get_vlounteer(volunteers):
            self.volunteersListView.hide_preloader()
            if volunteers:
                self.volunteersListView.set_volunteers(volunteers)
            else:
                self.error("No volunteers found")

        # Create a worker to call the async function
        worker = Worker(lambda: self.model.get_all_volunteers())
        worker.result_signal.connect(get_vlounteer)
        worker.error_signal.connect(self.error)
        worker.start()

    def remove_volunteer(self, volunteer):
        # Create a worker to call the async function
        worker = Worker(lambda: self.model.delete_volunteer(volunteer))
        worker.result_signal.connect(self.volunteersListView.delete_volunteer(volunteer.id))
        worker.error_signal.connect(self.error)
        worker.start()
        # Proceed to save the volunteer

    def add_update_volunteer(self, volunteer):
        # Save volunteer asynchronously
        if volunteer.id == 0:
            worker = Worker(lambda: self.model.add_volunteer(volunteer))
            worker.result_signal.connect(self.volunteersListView.add_volunteer)
            worker.error_signal.connect(self.error)
            worker.start()
        else:
            worker = Worker(lambda: self.model.update_volunteer(volunteer))
            worker.result_signal.connect(self.volunteersListView.update_volunteer)
            worker.error_signal.connect(self.error)
            worker.start()

    def add_observer_to_add_volunteer(self, action):
        self.volunteersListView.addVolunteerClicked.connect(action)
        self.volunteersListView.updateVolunteerClicked.connect(action)

    def error(self, message):
        print(message)
        self.errorSignal.emit(message)
