
class ShellController:
    def __init__(self, shellView):
        print("ShellController init")
        self.shellView = shellView
        self.shellView.showEventsClicked.connect(lambda: self.show_events_list())
        self.shellView.showVolunteersClicked.connect(lambda : self.show_volunteers_list())

    def show_events_list(self):
        print("show events list")
        self.shellView.show_events_list()

    def show_volunteers_list(self):
        self.shellView.show_volunteers_list()

    def show_map(self):
        self.shellView.show_map()