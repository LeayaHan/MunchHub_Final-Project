from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Admin.AdminComponents import StyledTable, ActionButton
import hashlib


class StaffManagementView(QWidget):
    """Staff Management View - Manage staff members"""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("Staff Management")
        title_label.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Add Staff button
        add_btn = QPushButton("Add Staff")
        add_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setMinimumHeight(40)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_btn.clicked.connect(self.add_staff)
        header_layout.addWidget(add_btn)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        refresh_btn.clicked.connect(self.load_staff)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Action buttons
        action_layout = QHBoxLayout()

        view_btn = ActionButton("View Details", "#2196F3")
        view_btn.clicked.connect(self.view_staff)
        action_layout.addWidget(view_btn)

        edit_btn = ActionButton("Edit Staff", "#FF9800")
        edit_btn.clicked.connect(self.edit_staff)
        action_layout.addWidget(edit_btn)

        delete_btn = ActionButton("Remove Staff", "#f44336")
        delete_btn.clicked.connect(self.delete_staff)
        action_layout.addWidget(delete_btn)

        action_layout.addStretch()
        layout.addLayout(action_layout)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search staff by name, username, or Staff ID...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        self.search_input.textChanged.connect(self.filter_staff)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Staff table
        self.staff_table = self.create_staff_table()
        layout.addWidget(self.staff_table)

        # Load initial data
        self.load_staff()

    def create_staff_table(self):
        """Create staff table"""
        table = StyledTable()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Staff ID", "First Name", "Middle Name", "Last Name", "Username", "Phone Number"
        ])

        # Enable single selection
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        return table

    def load_staff(self):
        """Load staff from database"""
        try:
            staff_list = self.controller.get_all_staff()
            self.staff_table.setRowCount(len(staff_list))

            for row, staff in enumerate(staff_list):
                # Staff ID
                id_item = QTableWidgetItem(staff['StaffID'])
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.staff_table.setItem(row, 0, id_item)

                # First Name
                first_name_item = QTableWidgetItem(staff['UFirstName'])
                self.staff_table.setItem(row, 1, first_name_item)

                # Middle Name
                middle_name_item = QTableWidgetItem(staff.get('UMiddleName') or "")
                self.staff_table.setItem(row, 2, middle_name_item)

                # Last Name
                last_name_item = QTableWidgetItem(staff['ULastName'])
                self.staff_table.setItem(row, 3, last_name_item)

                # Username
                username_item = QTableWidgetItem(staff['Username'])
                self.staff_table.setItem(row, 4, username_item)

                # Phone Number
                phone_item = QTableWidgetItem(staff.get('PhoneNum', 'N/A'))
                phone_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.staff_table.setItem(row, 5, phone_item)

        except Exception as e:
            self.show_message("Error", f"Error loading staff: {e}", "critical")

    def filter_staff(self, search_text):
        """Filter staff by search text"""
        for row in range(self.staff_table.rowCount()):
            match = False
            for col in range(6):  # Search in all columns
                item = self.staff_table.item(row, col)
                if item and search_text.lower() in item.text().lower():
                    match = True
                    break
            self.staff_table.setRowHidden(row, not match)

    def add_staff(self):
        """Open dialog to add new staff"""
        dialog = AddStaffDialog(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_staff()

    def view_staff(self):
        """View staff details"""
        selected_row = self.staff_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a staff member to view.", "warning")
            return

        staff_id = self.staff_table.item(selected_row, 0).text()
        first_name = self.staff_table.item(selected_row, 1).text()
        middle_name = self.staff_table.item(selected_row, 2).text()
        last_name = self.staff_table.item(selected_row, 3).text()
        username = self.staff_table.item(selected_row, 4).text()
        phone = self.staff_table.item(selected_row, 5).text()

        dialog = StaffDetailsDialog(
            staff_id, first_name, middle_name, last_name, username, phone, parent=self
        )
        dialog.exec()

    def edit_staff(self):
        """Edit staff information"""
        selected_row = self.staff_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a staff member to edit.", "warning")
            return

        staff_id = self.staff_table.item(selected_row, 0).text()
        first_name = self.staff_table.item(selected_row, 1).text()
        middle_name = self.staff_table.item(selected_row, 2).text()
        last_name = self.staff_table.item(selected_row, 3).text()
        username = self.staff_table.item(selected_row, 4).text()
        phone = self.staff_table.item(selected_row, 5).text()

        dialog = EditStaffDialog(
            self.controller, staff_id, first_name, middle_name, last_name, username, phone, parent=self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_staff()

    def delete_staff(self):
        """Delete selected staff member"""
        selected_row = self.staff_table.currentRow()
        if selected_row < 0:
            self.show_message("No Selection", "Please select a staff member to remove.", "warning")
            return

        staff_id = self.staff_table.item(selected_row, 0).text()
        staff_name = f"{self.staff_table.item(selected_row, 1).text()} {self.staff_table.item(selected_row, 3).text()}"

        # Apply message box styling
        self.apply_message_box_style()

        reply = QMessageBox.question(
            self,
            'Confirm Remove',
            f'Are you sure you want to remove staff member "{staff_name}"?\n\nThis action cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete_staff(staff_id)
            if success:
                self.show_message("Success", message, "information")
                self.load_staff()
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


class AddStaffDialog(QDialog):
    """Dialog to add new staff member"""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add New Staff Member")
        self.setMinimumWidth(550)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_label = QLabel("Add New Staff Member")
        header_label.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #003274;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        # Form frame
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e6e6e6;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_frame.setLayout(form_layout)

        # Input style
        input_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 13px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """

        label_style = "font-size: 13px; color: #333; font-weight: bold;"

        # Username
        username_label = QLabel("Username:*")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet(input_style)

        # Set validator to prevent spaces in username
        username_validator = QRegularExpressionValidator(QRegularExpression("[^\\s]*"))
        self.username_input.setValidator(username_validator)

        form_layout.addRow(username_label, self.username_input)

        # Password
        password_label = QLabel("Password:*")
        password_label.setStyleSheet(label_style)

        password_container = QHBoxLayout()
        password_container.setSpacing(5)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        password_container.addWidget(self.password_input)

        # Toggle password visibility button
        self.toggle_password_btn = QPushButton("Show")
        self.toggle_password_btn.setFixedSize(60, 40)
        self.toggle_password_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        password_container.addWidget(self.toggle_password_btn)

        form_layout.addRow(password_label, password_container)

        # First Name
        fname_label = QLabel("First Name:*")
        fname_label.setStyleSheet(label_style)
        self.fname_input = QLineEdit()
        self.fname_input.setPlaceholderText("Enter first name")
        self.fname_input.setStyleSheet(input_style)
        form_layout.addRow(fname_label, self.fname_input)

        # Middle Name
        mname_label = QLabel("Middle Name:")
        mname_label.setStyleSheet(label_style)
        self.mname_input = QLineEdit()
        self.mname_input.setPlaceholderText("Enter middle name (optional)")
        self.mname_input.setStyleSheet(input_style)
        form_layout.addRow(mname_label, self.mname_input)

        # Last Name
        lname_label = QLabel("Last Name:*")
        lname_label.setStyleSheet(label_style)
        self.lname_input = QLineEdit()
        self.lname_input.setPlaceholderText("Enter last name")
        self.lname_input.setStyleSheet(input_style)
        form_layout.addRow(lname_label, self.lname_input)

        # Phone Number
        phone_label = QLabel("Phone Number:*")
        phone_label.setStyleSheet(label_style)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number (11 digits)")
        self.phone_input.setMaxLength(11)
        self.phone_input.setStyleSheet(input_style)

        # Set validator to only accept numbers
        phone_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.phone_input.setValidator(phone_validator)

        form_layout.addRow(phone_label, self.phone_input)

        layout.addWidget(form_frame)

        # Required fields note
        note_label = QLabel("* Required fields")
        note_label.setStyleSheet("color: #666; font-size: 11px; font-style: italic;")
        layout.addWidget(note_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Add Staff")
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_staff)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setText("Show")

    def save_staff(self):
        """Save new staff member"""
        # Get values
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        first_name = self.fname_input.text().strip()
        middle_name = self.mname_input.text().strip()
        last_name = self.lname_input.text().strip()
        phone = self.phone_input.text().strip()

        # Apply message box styling
        self.apply_message_box_style()

        # Validation
        if not username or not password or not first_name or not last_name or not phone:
            QMessageBox.warning(self, "Missing Information", "Please fill in all required fields.")
            return

        if len(phone) != 11 or not phone.isdigit():
            QMessageBox.warning(self, "Invalid Phone", "Phone number must be exactly 11 digits.")
            return

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Add staff through controller with hashed password
        success, message = self.controller.add_staff(
            username, hashed_password, first_name, middle_name, last_name, phone
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


class EditStaffDialog(QDialog):
    """Dialog to edit staff information"""

    def __init__(self, controller, staff_id, first_name, middle_name, last_name, username, phone, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.staff_id = staff_id
        self.original_username = username
        self.initUI(first_name, middle_name, last_name, username, phone)

    def initUI(self, first_name, middle_name, last_name, username, phone):
        self.setWindowTitle(f"Edit Staff - {self.staff_id}")
        self.setMinimumWidth(550)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_label = QLabel(f"Edit Staff - {self.staff_id}")
        header_label.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #003274;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        # Form frame
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e6e6e6;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_frame.setLayout(form_layout)

        input_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 13px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """

        label_style = "font-size: 13px; color: #333; font-weight: bold;"

        # First Name
        fname_label = QLabel("First Name:*")
        fname_label.setStyleSheet(label_style)
        self.fname_input = QLineEdit(first_name)
        self.fname_input.setStyleSheet(input_style)
        form_layout.addRow(fname_label, self.fname_input)

        # Middle Name
        mname_label = QLabel("Middle Name:")
        mname_label.setStyleSheet(label_style)
        self.mname_input = QLineEdit(middle_name)
        self.mname_input.setStyleSheet(input_style)
        form_layout.addRow(mname_label, self.mname_input)

        # Last Name
        lname_label = QLabel("Last Name:*")
        lname_label.setStyleSheet(label_style)
        self.lname_input = QLineEdit(last_name)
        self.lname_input.setStyleSheet(input_style)
        form_layout.addRow(lname_label, self.lname_input)

        # Phone Number
        phone_label = QLabel("Phone Number:*")
        phone_label.setStyleSheet(label_style)
        self.phone_input = QLineEdit(phone)
        self.phone_input.setMaxLength(11)
        self.phone_input.setStyleSheet(input_style)

        # Set validator to only accept numbers
        phone_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.phone_input.setValidator(phone_validator)

        form_layout.addRow(phone_label, self.phone_input)

        layout.addWidget(form_frame)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save Changes")
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_changes)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

    def save_changes(self):
        """Save staff changes"""
        first_name = self.fname_input.text().strip()
        middle_name = self.mname_input.text().strip()
        last_name = self.lname_input.text().strip()
        phone = self.phone_input.text().strip()

        # Apply message box styling
        self.apply_message_box_style()

        if not first_name or not last_name or not phone:
            QMessageBox.warning(self, "Missing Information", "Please fill in all required fields.")
            return

        if len(phone) != 11 or not phone.isdigit():
            QMessageBox.warning(self, "Invalid Phone", "Phone number must be exactly 11 digits.")
            return

        success, message = self.controller.update_staff(
            self.staff_id, first_name, middle_name, last_name, phone
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


class StaffDetailsDialog(QDialog):
    """Dialog to view staff details"""

    def __init__(self, staff_id, first_name, middle_name, last_name, username, phone, parent=None):
        super().__init__(parent)
        self.staff_id = staff_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Staff Details - {self.staff_id}")
        self.setMinimumWidth(550)
        self.setMinimumHeight(450)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)

        name_label = QLabel(f"{self.first_name} {self.middle_name} {self.last_name}".replace("  ", " "))
        name_label.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #003274;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(name_label)

        id_label = QLabel(f"Staff ID: {self.staff_id}")
        id_label.setFont(QFont('Arial', 13))
        id_label.setStyleSheet("color: #666;")
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(id_label)

        layout.addLayout(header_layout)

        # Details frame
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e6e6e6;
            }
        """)
        details_layout = QFormLayout()
        details_layout.setContentsMargins(30, 30, 30, 30)
        details_layout.setSpacing(20)
        details_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        details_frame.setLayout(details_layout)

        detail_style = "font-size: 14px; color: #000000; font-weight: bold;"
        label_style = "font-size: 13px; color: #666; font-weight: bold;"

        # First Name
        first_name_value = QLabel(self.first_name)
        first_name_value.setStyleSheet(detail_style)
        first_name_label = QLabel("First Name:")
        first_name_label.setStyleSheet(label_style)
        details_layout.addRow(first_name_label, first_name_value)

        # Middle Name
        if self.middle_name:
            middle_name_value = QLabel(self.middle_name)
            middle_name_value.setStyleSheet(detail_style)
            middle_name_label = QLabel("Middle Name:")
            middle_name_label.setStyleSheet(label_style)
            details_layout.addRow(middle_name_label, middle_name_value)

        # Last Name
        last_name_value = QLabel(self.last_name)
        last_name_value.setStyleSheet(detail_style)
        last_name_label = QLabel("Last Name:")
        last_name_label.setStyleSheet(label_style)
        details_layout.addRow(last_name_label, last_name_value)

        # Username
        username_value = QLabel(self.username)
        username_value.setStyleSheet(detail_style)
        username_label = QLabel("Username:")
        username_label.setStyleSheet(label_style)
        details_layout.addRow(username_label, username_value)

        # Phone Number
        phone_value = QLabel(self.phone if self.phone != 'N/A' else 'Not provided')
        phone_value.setStyleSheet(detail_style)
        phone_label = QLabel("Phone Number:")
        phone_label.setStyleSheet(label_style)
        details_layout.addRow(phone_label, phone_value)

        layout.addWidget(details_frame)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(45)
        close_btn.setMaximumWidth(150)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)