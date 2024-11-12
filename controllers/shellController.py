from PySide6.QtCore import QTimer


class ShellController:
    def __init__(self, shellView):
        self.shellView = shellView
        # Connect buttons to methods
        self.shellView.showEventsClicked.connect(lambda: self.show_events_list())
        self.shellView.showVolunteersClicked.connect(
            lambda: self.show_volunteers_list()
        )
        self.shellView.goBackClicked.connect(lambda: self.show_map_and_event())

    # Define methods to show views
    def show_events_list(self):
        self.shellView.show_events_list()

    def show_volunteers_list(self):
        self.shellView.show_volunteers_list()

    def show_map_and_event(self):
        self.shellView.show_map_and_event()

    # Define error method for status bar
    def error(self, message):
        # Set status bar red
        self.shellView.statusBar.setStyleSheet("background-color: red; color: white;")
        self.shellView.statusBar.showMessage(message)

        # Use a QTimer with a lambda to reset the style after 5 seconds
        QTimer.singleShot(5000, lambda: (
            self.shellView.statusBar.setStyleSheet("background-color: black; color: white;"),
            self.shellView.statusBar.clearMessage()
        ))

