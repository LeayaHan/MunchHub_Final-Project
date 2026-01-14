from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Admin.AdminComponents import StyledTable, ActionButton, get_input_style


class MenuManagementView(QWidget):
    """Menu Management View - Manage menu items and categories"""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header with tabs
        header_layout = QHBoxLayout()

        title_label = QLabel("Menu Management")
        title_label.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Tab widget for Menu Items and Categories
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e6e6e6;
                background-color: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                color: #000000;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #003274;
            }
            QTabBar::tab:hover {
                background-color: #e0e0e0;
            }
        """)

        # Menu Items Tab
        menu_items_widget = self.create_menu_items_tab()
        self.tab_widget.addTab(menu_items_widget, "Menu Items")

        # Categories Tab
        categories_widget = self.create_categories_tab()
        self.tab_widget.addTab(categories_widget, "Categories")

        layout.addWidget(self.tab_widget)

    def create_menu_items_tab(self):
        """Create menu items management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        widget.setLayout(layout)

        # Action buttons
        action_layout = QHBoxLayout()

        add_btn = ActionButton("Add Menu Item", "#4CAF50")
        add_btn.clicked.connect(self.add_menu_item)
        action_layout.addWidget(add_btn)

        edit_btn = ActionButton("Edit Selected", "#2196F3")
        edit_btn.clicked.connect(self.edit_menu_item)
        action_layout.addWidget(edit_btn)

        delete_btn = ActionButton("Delete Selected", "#f44336")
        delete_btn.clicked.connect(self.delete_menu_item)
        action_layout.addWidget(delete_btn)

        refresh_btn = ActionButton("Refresh", "#FF9800")
        refresh_btn.clicked.connect(self.load_menu_items)
        action_layout.addWidget(refresh_btn)

        action_layout.addStretch()
        layout.addLayout(action_layout)

        # Search bar
        search_layout = QHBoxLayout()
        self.menu_search_input = QLineEdit()
        self.menu_search_input.setPlaceholderText("Search menu items...")
        self.menu_search_input.setMinimumHeight(40)
        self.menu_search_input.setStyleSheet("color:black;")
        self.menu_search_input.textChanged.connect(self.filter_menu_items)
        search_layout.addWidget(self.menu_search_input)
        layout.addLayout(search_layout)

        # Menu items table
        self.menu_table = self.create_menu_table()
        layout.addWidget(self.menu_table)

        # Load initial data
        self.load_menu_items()

        return widget

    def create_menu_table(self):
        """Create menu items table"""
        table = StyledTable()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Menu ID", "Item Name", "Category", "Price", "Available"])

        # Enable single selection
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Set equal column widths
        header = table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Enable word wrap for better visibility
        table.setWordWrap(True)
        table.setTextElideMode(Qt.TextElideMode.ElideNone)

        return table

    def load_menu_items(self):
        """Load menu items from database"""
        try:
            items = self.controller.get_all_menu_items()
            self.menu_table.setRowCount(0)  # Clear table

            for item in items:
                row = self.menu_table.rowCount()
                self.menu_table.insertRow(row)

                # Menu ID
                id_item = QTableWidgetItem(item['MenuID'])
                id_item.setFont(QFont('Arial', 11))
                id_item.setForeground(QColor('#000000'))
                self.menu_table.setItem(row, 0, id_item)

                # Item Name
                name_item = QTableWidgetItem(item['ItemName'])
                name_item.setFont(QFont('Arial', 11))
                name_item.setForeground(QColor('#000000'))
                self.menu_table.setItem(row, 1, name_item)

                # Category
                category_item = QTableWidgetItem(item['CategoryName'])
                category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                category_item.setFont(QFont('Arial', 11))
                category_item.setForeground(QColor('#000000'))
                self.menu_table.setItem(row, 2, category_item)

                # Price
                price = float(item['Price']) if item['Price'] is not None else 0.0
                price_item = QTableWidgetItem(f"₱{price:.2f}")
                price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                price_item.setFont(QFont('Arial', 11))
                price_item.setForeground(QColor('#000000'))
                self.menu_table.setItem(row, 3, price_item)

                # Available
                available_item = QTableWidgetItem("Yes" if item['isAvailable'] else "No")
                available_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if item['isAvailable']:
                    available_item.setForeground(QColor('#4CAF50'))
                else:
                    available_item.setForeground(QColor('#f44336'))
                available_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
                self.menu_table.setItem(row, 4, available_item)

        except Exception as e:
            self.show_message("Error", f"Error loading menu items: {e}", "critical")
            import traceback
            traceback.print_exc()

    def filter_menu_items(self, search_text):
        """Filter menu items by search text"""
        for row in range(self.menu_table.rowCount()):
            match = False
            for col in range(3):  # Search in ID, Name, Category
                item = self.menu_table.item(row, col)
                if item and search_text.lower() in item.text().lower():
                    match = True
                    break
            self.menu_table.setRowHidden(row, not match)

    def add_menu_item(self):
        """Show dialog to add new menu item"""
        dialog = MenuItemDialog(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_menu_items()

    def edit_menu_item(self):
        """Edit selected menu item"""
        selected_row = self.menu_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a menu item to edit.", "warning")
            return

        menu_id = self.menu_table.item(selected_row, 0).text()
        dialog = MenuItemDialog(self.controller, menu_id=menu_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_menu_items()

    def delete_menu_item(self):
        """Delete selected menu item"""
        selected_row = self.menu_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a menu item to delete.", "warning")
            return

        menu_id = self.menu_table.item(selected_row, 0).text()
        item_name = self.menu_table.item(selected_row, 1).text()

        # Apply message box styling
        self.apply_message_box_style()

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Are you sure you want to delete "{item_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete_menu_item(menu_id)
            if success:
                self.show_message("Success", message, "information")
                self.load_menu_items()
            else:
                self.show_message("Error", message, "critical")

    def create_categories_tab(self):
        """Create categories management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        widget.setLayout(layout)

        # Action buttons
        action_layout = QHBoxLayout()

        add_btn = ActionButton("Add Category", "#4CAF50")
        add_btn.clicked.connect(self.add_category)
        action_layout.addWidget(add_btn)

        edit_btn = ActionButton("Edit Selected", "#2196F3")
        edit_btn.clicked.connect(self.edit_category)
        action_layout.addWidget(edit_btn)

        delete_btn = ActionButton("Delete Selected", "#f44336")
        delete_btn.clicked.connect(self.delete_category)
        action_layout.addWidget(delete_btn)

        refresh_btn = ActionButton("Refresh", "#FF9800")
        refresh_btn.clicked.connect(self.load_categories)
        action_layout.addWidget(refresh_btn)

        action_layout.addStretch()
        layout.addLayout(action_layout)

        # Categories table
        self.category_table = self.create_category_table()
        layout.addWidget(self.category_table)

        # Load initial data
        self.load_categories()

        return widget

    def create_category_table(self):
        """Create categories table"""
        table = StyledTable()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Category ID", "Category Name", "Description"])

        # Enable single selection
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Set equal column widths
        header = table.horizontalHeader()
        for i in range(3):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Enable word wrap for better visibility
        table.setWordWrap(True)
        table.setTextElideMode(Qt.TextElideMode.ElideNone)

        return table

    def load_categories(self):
        """Load categories from database"""
        try:
            categories = self.controller.get_all_categories()
            self.category_table.setRowCount(0)  # Clear table

            for category in categories:
                row = self.category_table.rowCount()
                self.category_table.insertRow(row)

                # Category ID
                id_item = QTableWidgetItem(category['CategoryID'])
                id_item.setFont(QFont('Arial', 11))
                id_item.setForeground(QColor('#000000'))
                self.category_table.setItem(row, 0, id_item)

                # Category Name
                name_item = QTableWidgetItem(category['CategoryName'])
                name_item.setFont(QFont('Arial', 11))
                name_item.setForeground(QColor('#000000'))
                self.category_table.setItem(row, 1, name_item)

                # Description
                desc_item = QTableWidgetItem(category['Description'] or "")
                desc_item.setFont(QFont('Arial', 11))
                desc_item.setForeground(QColor('#000000'))
                self.category_table.setItem(row, 2, desc_item)

        except Exception as e:
            self.show_message("Error", f"Error loading categories: {e}", "critical")
            import traceback
            traceback.print_exc()

    def add_category(self):
        """Show dialog to add new category"""
        dialog = CategoryDialog(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()

    def edit_category(self):
        """Edit selected category"""
        selected_row = self.category_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a category to edit.", "warning")
            return

        category_id = self.category_table.item(selected_row, 0).text()
        dialog = CategoryDialog(self.controller, category_id=category_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()

    def delete_category(self):
        """Delete selected category"""
        selected_row = self.category_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a category to delete.", "warning")
            return

        category_id = self.category_table.item(selected_row, 0).text()
        category_name = self.category_table.item(selected_row, 1).text()

        # Apply message box styling
        self.apply_message_box_style()

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Are you sure you want to delete category "{category_name}"?\n\nWarning: This may affect menu items in this category.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete_category(category_id)
            if success:
                self.show_message("Success", message, "information")
                self.load_categories()
            else:
                self.show_message("Error", message, "critical")

    def apply_message_box_style(self):
        """Apply black text styling to message boxes"""
        QApplication.instance().setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 11px;
            }
            QMessageBox QPushButton {
                color: black;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 4px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)

    def show_message(self, title, message, msg_type):
        """Show message box with proper styling"""
        self.apply_message_box_style()

        if msg_type == "information":
            QMessageBox.information(self, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self, title, message)
        elif msg_type == "critical":
            QMessageBox.critical(self, title, message)


class MenuItemDialog(QDialog):
    """Dialog for adding/editing menu items"""

    def __init__(self, controller, menu_id=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.menu_id = menu_id
        self.is_edit = menu_id is not None
        self.initUI()

        if self.is_edit:
            self.load_menu_item()

    def initUI(self):
        self.setWindowTitle("Edit Menu Item" if self.is_edit else "Add Menu Item")
        self.setMinimumWidth(500)
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.setLayout(layout)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Menu ID - Only show in edit mode, auto-generated in add mode
        if self.is_edit:
            self.menu_id_label = QLabel(self.menu_id)
            self.menu_id_label.setMinimumHeight(40)
            self.menu_id_label.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border: 2px solid #e0e0e0;
                    border-radius: 5px;
                    font-size: 13px;
                    background-color: #f0f0f0;
                    color: #333;
                }
            """)
            label = QLabel("Menu ID:")
            label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
            form_layout.addRow(label, self.menu_id_label)
        else:
            auto_id_label = QLabel("(Auto-generated)")
            auto_id_label.setStyleSheet("color: #666; font-style: italic; font-size: 12px;")
            label = QLabel("Menu ID:")
            label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
            form_layout.addRow(label, auto_id_label)

        # Item Name
        self.name_input = QLineEdit()
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 13px;
                background-color: #f9f9f9;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: #ffffff;
            }
        """)
        label = QLabel("Item Name:")
        label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
        form_layout.addRow(label, self.name_input)

        # Category
        self.category_combo = QComboBox()
        self.category_combo.setMinimumHeight(40)
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 13px;
                background-color: #f9f9f9;
                color: #333;
            }
            QComboBox:focus {
                border: 2px solid #2196F3;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
        """)
        self.load_categories()
        label = QLabel("Category:")
        label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
        form_layout.addRow(label, self.category_combo)

        # Price
        self.price_input = QLineEdit()
        self.price_input.setMinimumHeight(40)
        self.price_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 13px;
                background-color: #f9f9f9;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: #ffffff;
            }
        """)
        self.price_input.setPlaceholderText("0.00")
        label = QLabel("Price (₱):")
        label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
        form_layout.addRow(label, self.price_input)

        # Available
        self.available_check = QCheckBox("Item is available for ordering")
        self.available_check.setChecked(True)
        self.available_check.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #e0e0e0;
                border-radius: 4px;
                background-color: #f9f9f9;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
        """)
        label = QLabel("Availability:")
        label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
        form_layout.addRow(label, self.available_check)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_btn = QPushButton("Save" if self.is_edit else "Add Item")
        save_btn.setMinimumHeight(45)
        save_btn.setMinimumWidth(140)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_menu_item)
        button_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setMinimumWidth(140)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41808;
            }
        """)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def load_categories(self):
        """Load categories into combo box"""
        categories = self.controller.get_all_categories()
        for category in categories:
            self.category_combo.addItem(category['CategoryName'], category['CategoryID'])

    def load_menu_item(self):
        """Load menu item data for editing"""
        item = self.controller.get_menu_item(self.menu_id)
        if item:
            self.name_input.setText(item['ItemName'])
            self.price_input.setText(str(item['Price']))
            self.available_check.setChecked(item['isAvailable'])

            # Set category
            index = self.category_combo.findData(item['CategoryID'])
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

    def save_menu_item(self):
        """Save menu item"""
        name = self.name_input.text().strip()
        category_id = self.category_combo.currentData()
        price = self.price_input.text().strip()
        is_available = self.available_check.isChecked()

        # Apply message box styling
        self.apply_message_box_style()

        # Validation
        if not name or not price:
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
            return

        try:
            price = float(price)
            if price < 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Invalid Price", "Please enter a valid price (numbers only).")
            return

        if self.is_edit:
            success, message = self.controller.update_menu_item(
                self.menu_id, category_id, name, price, is_available
            )
        else:
            success, message = self.controller.add_menu_item(
                category_id, name, price, is_available
            )

        if success:
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)

    def apply_message_box_style(self):
        """Apply black text styling to message boxes"""
        QApplication.instance().setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 11px;
            }
            QMessageBox QPushButton {
                color: black;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 4px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)


class CategoryDialog(QDialog):
    """Dialog for adding/editing categories"""

    def __init__(self, controller, category_id=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.category_id = category_id
        self.is_edit = category_id is not None
        self.initUI()

        if self.is_edit:
            self.load_category()

    def initUI(self):
        self.setWindowTitle("Edit Category" if self.is_edit else "Add Category")
        self.setMinimumWidth(500)
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.setLayout(layout)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Category ID - Only show in edit mode, auto-generated in add mode
        if self.is_edit:
            self.category_id_label = QLabel(self.category_id)
            self.category_id_label.setMinimumHeight(40)
            self.category_id_label.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border: 2px solid #e0e0e0;
                    border-radius: 5px;
                    font-size: 13px;
                    background-color: #f0f0f0;
                    color: #333;
                }
            """)
            label = QLabel("Category ID:")
            label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
            form_layout.addRow(label, self.category_id_label)
        else:
            auto_id_label = QLabel("(Auto-generated)")
            auto_id_label.setStyleSheet("color: #666; font-style: italic; font-size: 12px;")
            label = QLabel("Category ID:")
            label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
            form_layout.addRow(label, auto_id_label)

        # Category Name
        self.name_input = QLineEdit()
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 13px;
                background-color: #f9f9f9;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: #ffffff;
            }
        """)
        label = QLabel("Category Name:")
        label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
        form_layout.addRow(label, self.name_input)

        # Description
        self.description_input = QTextEdit()
        self.description_input.setMinimumHeight(100)
        self.description_input.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 13px;
                background-color: #f9f9f9;
                color: #333;
            }
            QTextEdit:focus {
                border: 2px solid #2196F3;
                background-color: #ffffff;
            }
        """)
        label = QLabel("Description:")
        label.setStyleSheet("color: #333; font-weight: bold; font-size: 13px;")
        form_layout.addRow(label, self.description_input)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_btn = QPushButton("Save" if self.is_edit else "Add Category")
        save_btn.setMinimumHeight(45)
        save_btn.setMinimumWidth(140)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_category)
        button_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setMinimumWidth(140)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41808;
            }
        """)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def load_category(self):
        """Load category data for editing"""
        category = self.controller.get_category(self.category_id)
        if category:
            self.name_input.setText(category['CategoryName'])
            self.description_input.setPlainText(category['Description'] or "")

    def save_category(self):
        """Save category"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()

        # Apply message box styling
        self.apply_message_box_style()

        # Validation
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a category name.")
            return

        if self.is_edit:
            success, message = self.controller.update_category(self.category_id, name, description)
        else:
            success, message = self.controller.add_category(name, description)

        if success:
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)

    def apply_message_box_style(self):
        """Apply black text styling to message boxes"""
        QApplication.instance().setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 11px;
            }
            QMessageBox QPushButton {
                color: black;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 4px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)