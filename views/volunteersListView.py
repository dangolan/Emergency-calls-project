from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QLineEdit,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon


class VolunteersListView(QWidget):
    def __init__(self):
        super().__init__()
        # Create the main vertical layout
        main_layout = QVBoxLayout(self)

        # Create a horizontal layout for the button and search input
        top_layout = QHBoxLayout()

        # Create a search input field (QLineEdit) for filtering
        self.searchInput = QLineEdit()
        self.searchInput.setObjectName("searchInput")
        self.searchInput.setPlaceholderText("Search for a volunteer...")
        self.searchInput.textChanged.connect(self.filter_items)
        top_layout.addWidget(self.searchInput)


        # Create a button and add it to the right side of the top layout
        self.addButton = QPushButton()
        self.addButton.clicked.connect(self.on_add_button_click)
        self.addButton.setObjectName("addButton")
        self.addButton.setIcon(QIcon("images/addBlack.png"))  # Set your add icon
        top_layout.addWidget(self.addButton)

        # Align the horizontal layout to the center
        top_layout.setAlignment(Qt.AlignCenter)

       
        main_layout.addLayout(top_layout)

        # Set the main layout as the layout for the widget
        self.setLayout(main_layout)


        # Create a QListWidget to hold the list of volunteers
        self.list_widget = QListWidget()

        # Store items in a separate list for filtering
        self.items_data = []
        for i in range(12):
            item_text = f"Volunteer {i + 1}"
            item_details = f"Details for Volunteer {i + 1}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, item_details)
            self.list_widget.addItem(item)
            self.items_data.append((item_text, item_details))  # Store text and details


        # Add the list widget to the layout
        main_layout.addWidget(self.list_widget)


        self.setLayout(main_layout)
        self.setWindowTitle("Volunteers List with Search")
        self.resize(400, 500)

        stylesheet = self.load_stylesheet("views/styles/volunteersList.qss")
        self.setStyleSheet(stylesheet)

    def print_selected_item(self):
        # Get the selected item
        current_item = self.list_widget.currentItem()
        if current_item:
            details = current_item.data(Qt.UserRole)
            print(f"Selected: {current_item.text()}, Details: {details}")
        else:
            print("No item selected.")

    def filter_items(self, search_text):
        # Clear the list widget before filtering
        self.list_widget.clear()

        # Filter items based on search text
        for item_text, item_details in self.items_data:
            if search_text.lower() in item_text.lower():
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, item_details)
                self.list_widget.addItem(item)

    def on_add_button_click(self):
        # Handle button click
        print("add button clicked!")

    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            return file.read()
