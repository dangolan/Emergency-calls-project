from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


class EventListView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout to center the label
        layout = QVBoxLayout()

        # Create the label and center it
        label = QLabel("Event List View")
        label.setStyleSheet("font-size: 24px; color: black;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

        # Create a QListWidget
        self.list_widget = QListWidget()

        # Add custom items with "Show" and "Remove" buttons
        for i in range(12):
            self.add_custom_item(f"Item {i + 1}", f"Details for Item {i + 1}")

        # Add the list widget to the layout
        layout.addWidget(self.list_widget)

        # Add a button to print selected item details
        self.button = QPushButton("Get Selected Item Details")
        self.button.clicked.connect(self.print_selected_item)
        layout.addWidget(self.button)

        # Set the layout for the widget
        self.setLayout(layout)
        self.setWindowTitle("Styled List Example")
        self.resize(400, 500)

    def add_custom_item(self, item_name, item_details):
        # Create a QListWidgetItem
        list_item = QListWidgetItem(self.list_widget)

        # Create a custom widget to hold the item label and buttons
        item_widget = QWidget()

        # Create a horizontal layout for the custom widget
        item_layout = QHBoxLayout()

        # Create a label for the item name
        item_label = QLabel(item_name)
        item_label.setAlignment(Qt.AlignLeft)

        # Create the "Show" button
        show_button = QPushButton("Show")
        show_button.clicked.connect(lambda: self.show_item(item_details))

        # Create the "Remove" button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_item(list_item))

        # Add the label and buttons to the item layout
        item_layout.addWidget(item_label)
        item_layout.addWidget(show_button)
        item_layout.addWidget(remove_button)

        # Set the layout for the custom widget
        item_widget.setLayout(item_layout)

        # Set the size hint of the list item based on the custom widget size
        list_item.setSizeHint(item_widget.sizeHint())

        # Add the custom widget to the list widget's item
        self.list_widget.setItemWidget(list_item, item_widget)

    def show_item(self, details):
        print(f"Showing details: {details}")

    def remove_item(self, list_item):
        # Remove the item from the list
        row = self.list_widget.row(list_item)
        self.list_widget.takeItem(row)

    def print_selected_item(self):
        # Get the selected item
        current_item = self.list_widget.currentItem()
        if current_item:
            widget = self.list_widget.itemWidget(current_item)
            if widget:
                label = widget.findChild(QLabel)
                if label:
                    print(f"Selected: {label.text()}")
        else:
            print("No item selected.")
