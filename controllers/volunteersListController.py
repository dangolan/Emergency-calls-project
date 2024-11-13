from PySide6.QtCore import QObject, Signal
from worker import Worker


class VolunteersListController(QObject):
    errorSignal = Signal(str)

    def __init__(self, volunteersModel=None, volunteersListView=None):
        super().__init__()
        self.model = volunteersModel
        self.view = volunteersListView

    def load_volunteer(self, volunteers):
        self.view.add_volunteer(volunteers)

        # Call the async function and wait for the result
        def get_vlounteer(volunteers):
            if volunteers:
                for volunteer in volunteers:
                    self.view.add_volunteer(volunteer)
                self.view.add_volunteer(volunteers)
            else:
                self.error("No volunteers found")

        # Create a worker to call the async function
        worker = Worker(lambda: self.model.get_all_volunteers())
        worker.result_signal.connect(get_vlounteer)
        worker.error_signal.connect(self.error)
        worker.start()
