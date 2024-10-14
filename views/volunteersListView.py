from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QLineEdit,
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon


class VolunteersListView(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the label and the button
        top_layout = QHBoxLayout()

        # Create the label for the view title
        label = QLabel("Volunteers List View")
        label.setStyleSheet("font-size: 24px; color: black;")
        label.setAlignment(Qt.AlignLeft)

        # Add the label to the horizontal layout
        top_layout.addWidget(label)

        # Create a button and add it to the right side of the top layout
        self.new_button = QPushButton()
        self.new_button.setIcon(QIcon("images\pluse.png"))  # Set your back arrow icon
        self.new_button.setIconSize(QSize(24, 24))  # Set the icon size
        self.new_button.setStyleSheet("background-color: transparent; border: None;")
        top_layout.addWidget(self.new_button)

        # Add some spacing between the label and the button
        top_layout.addStretch()

        # Add the top layout to the main layout
        main_layout.addLayout(top_layout)

        # Create a search input field (QLineEdit) for filtering
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for a volunteer...")
        self.search_input.textChanged.connect(self.filter_items)
        main_layout.addWidget(self.search_input)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

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

        # Set styles for the list widget
        self.list_widget.setStyleSheet(
            """
            QListWidget {
                background-color: #f0f0f0;  /* Light gray background */
                border: 1px solid #cccccc;  /* Light gray border */
                font-size: 14px;  /* Font size */
            }
            QListWidget::item {
                padding: 30px;  /* Padding for each item */
                border-bottom: 1px solid #dddddd;  /* Bottom border for each item */
            }
            QListWidget::item:selected {
                background-color: #007BFF;  /* Blue background for selected item */
                color: white;  /* White text for selected item */
            }
        """
        )

        # Add the list widget to the layout
        main_layout.addWidget(self.list_widget)

        # Add a button to print selected item details
        self.button = QPushButton("Get Selected Item Details")
        self.button.clicked.connect(self.print_selected_item)
        main_layout.addWidget(self.button)

        self.setLayout(main_layout)
        self.setWindowTitle("Volunteers List with Search")
        self.resize(400, 500)

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

    def on_button_click(self):
        # Handle button click
        print("New button clicked!")
