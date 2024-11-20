from PySide6.QtCore import QObject, Signal
from worker import Worker


class VolunteersListController(QObject):
    errorSignal = Signal(str)

    def __init__(self, volunteersListView=None, volunteersModel=None, shellView=None):
        super().__init__()
        print("VolunteersListController")
        self.view = volunteersListView
        self.model = volunteersModel
        self.view.remove_volunteer_signal.connect(self.remove_volunteer)
        self.view.update_volunteer_signal.connect(self.update_volunteer)
        self.view.addVolunteerClicked.connect(self.add_volunteer)
        self.load_volunteer()

    def load_volunteer(self):
        # Call the async function and wait for the result
        self.view.show_preloader()

        def get_vlounteer(volunteers):
            self.view.hide_preloader()
            if volunteers:
                self.view.set_volunteers(volunteers)
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
        worker.result_signal.connect(self.view.delete_volunteer)
        worker.error_signal.connect(self.error)
        worker.start()

    def add_volunteer(self, volunteer):
        worker = Worker(lambda: self.model.add_volunteer(volunteer))
        worker.result_signal.connect(self.view.add_volunteer)
        worker.error_signal.connect(self.error)
        worker.start()

    def update_volunteer(self, volunteer):
        worker = Worker(lambda: self.model.update_volunteer(volunteer))
        worker.result_signal.connect(self.view.update_volunteer)
        worker.error_signal.connect(self.error)
        worker.start()

    def add_observer_to_add_volunteer(self, action):
        self.view.addVolunteerClicked.connect(action)

    def error(self, message):
        print(message)
        self.errorSignal.emit(message)
