import re
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class PhoneNumberValidator(QValidator):
    """Custom validator for phone numbers - only allows digits and max 11 characters"""

    def validate(self, text, pos):
        # Remove any non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, text))

        if len(digits_only) > 11:
            return QValidator.State.Invalid, text[:pos - 1], pos - 1

        if text and not text.replace(' ', '').isdigit():
            return QValidator.State.Invalid, text[:pos - 1], pos - 1

        if len(digits_only) == 11:
            return QValidator.State.Acceptable, text, pos
        elif len(digits_only) == 0:
            return QValidator.State.Intermediate, text, pos
        else:
            return QValidator.State.Intermediate, text, pos


class SignUpWindow(QDialog):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.password_visible = False
        self.confirm_password_visible = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MunchHub - Sign Up')
        self.setFixedSize(550, 820)  # Increased height for better spacing
        self.setModal(True)

        # Set window background color
        self.setStyleSheet("background-color: #f5f5f5;")

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Scroll area for the form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")

        # Sign up container frame
        signup_frame = QFrame()
        signup_frame.setStyleSheet("""
            QFrame {
                background-color: #003274;
                border-radius: 15px;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        signup_frame.setGraphicsEffect(shadow)

        # Sign up frame layout
        signup_layout = QVBoxLayout()
        signup_layout.setContentsMargins(40, 30, 40, 30)
        signup_layout.setSpacing(10)  # Consistent spacing
        signup_frame.setLayout(signup_layout)

        # Header
        header_label = QLabel('Create Account')
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(header_label)

        subtitle_label = QLabel('Join MunchHub today!')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont('Arial', 11))
        subtitle_label.setStyleSheet("color: #fcfffd; margin-bottom: 10px;")
        signup_layout.addWidget(subtitle_label)

        signup_layout.addSpacing(10)

        # First Name field
        firstname_label = QLabel('First Name *')
        firstname_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        firstname_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(firstname_label)

        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText('Enter your first name')
        self.firstname_input.setFont(QFont('Arial', 11))
        self.firstname_input.setMinimumHeight(40)
        self.firstname_input.setStyleSheet(self.get_input_style())
        signup_layout.addWidget(self.firstname_input)

        # Middle Name field (optional)
        middlename_label = QLabel('Middle Name (Optional)')
        middlename_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        middlename_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(middlename_label)

        self.middlename_input = QLineEdit()
        self.middlename_input.setPlaceholderText('Enter your middle name')
        self.middlename_input.setFont(QFont('Arial', 11))
        self.middlename_input.setMinimumHeight(40)
        self.middlename_input.setStyleSheet(self.get_input_style())
        signup_layout.addWidget(self.middlename_input)

        # Last Name field
        lastname_label = QLabel('Last Name *')
        lastname_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        lastname_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(lastname_label)

        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText('Enter your last name')
        self.lastname_input.setFont(QFont('Arial', 11))
        self.lastname_input.setMinimumHeight(40)
        self.lastname_input.setStyleSheet(self.get_input_style())
        signup_layout.addWidget(self.lastname_input)

        # Username field
        username_label = QLabel('Username *')
        username_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Choose a username (no spaces)')
        self.username_input.setFont(QFont('Arial', 11))
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet(self.get_input_style())
        self.username_input.textChanged.connect(self.validate_username)
        signup_layout.addWidget(self.username_input)

        # Phone Number field
        phone_label = QLabel('Phone Number * (11 digits)')
        phone_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        phone_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(phone_label)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('09XXXXXXXXX')
        self.phone_input.setFont(QFont('Arial', 11))
        self.phone_input.setMinimumHeight(40)
        self.phone_input.setMaxLength(11)
        self.phone_input.setStyleSheet(self.get_input_style())
        # Set validator to only allow numbers
        self.phone_input.setValidator(PhoneNumberValidator())
        self.phone_input.textChanged.connect(self.validate_phone)
        signup_layout.addWidget(self.phone_input)

        # Password field with toggle
        password_label = QLabel('Password * (min 6 characters)')
        password_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(password_label)

        password_container = QHBoxLayout()
        password_container.setSpacing(0)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Create a strong password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont('Arial', 11))
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px 0px 0px 8px;
                background-color: #fafafa;
                color: #333;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #f0b03f;
                background-color: white;
            }
        """)

        self.password_toggle = QPushButton('show')
        self.password_toggle.setFixedSize(40, 40)
        self.password_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.password_toggle.setStyleSheet("""
            QPushButton {
                background-color: #fafafa;
                border: 2px solid #e0e0e0;
                border-left: none;
                border-radius: 0px 8px 8px 0px;
                font-size: 14px;
                color: black;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.password_toggle.clicked.connect(self.toggle_password_visibility)

        password_container.addWidget(self.password_input)
        password_container.addWidget(self.password_toggle)
        signup_layout.addLayout(password_container)

        # Confirm Password field with toggle
        confirm_password_label = QLabel('Confirm Password *')
        confirm_password_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        confirm_password_label.setStyleSheet("color: #fcfffd;")
        signup_layout.addWidget(confirm_password_label)

        confirm_password_container = QHBoxLayout()
        confirm_password_container.setSpacing(0)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Re-enter your password')
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setFont(QFont('Arial', 11))
        self.confirm_password_input.setMinimumHeight(40)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px 0px 0px 8px;
                background-color: #fafafa;
                color: #333;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #f0b03f;
                background-color: white;
            }
        """)

        self.confirm_password_toggle = QPushButton('show')
        self.confirm_password_toggle.setFixedSize(40, 40)
        self.confirm_password_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_password_toggle.setStyleSheet("""
            QPushButton {
                background-color: #fafafa;
                border: 2px solid #e0e0e0;
                border-left: none;
                border-radius: 0px 8px 8px 0px;
                font-size: 14px;
                color: black;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.confirm_password_toggle.clicked.connect(self.toggle_confirm_password_visibility)

        confirm_password_container.addWidget(self.confirm_password_input)
        confirm_password_container.addWidget(self.confirm_password_toggle)
        signup_layout.addLayout(confirm_password_container)

        signup_layout.addSpacing(15)

        # Sign Up button
        signup_button = QPushButton('Sign Up')
        signup_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        signup_button.setCursor(Qt.CursorShape.PointingHandCursor)
        signup_button.setMinimumHeight(45)
        signup_button.setStyleSheet("""
            QPushButton {
                background-color: #f0b03f;
                color: #000a03;
                padding: 12px;
                border-radius: 8px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffc14d;
            }
            QPushButton:pressed {
                background-color: #d99a2f;
            }
        """)
        signup_button.clicked.connect(self.handle_signup)
        signup_layout.addWidget(signup_button)

        # Login link
        login_container = QHBoxLayout()
        login_text = QLabel("Already have an account?")
        login_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        login_text.setFont(QFont('Arial', 9))
        login_text.setStyleSheet("color: #f5f7f6;")

        login_link = QLabel('<a href="#" style="color: #1a3a6b; text-decoration: none; font-weight: bold;">Login</a>')
        login_link.setAlignment(Qt.AlignmentFlag.AlignLeft)
        login_link.setFont(QFont('Arial', 9))
        login_link.setOpenExternalLinks(False)
        login_link.linkActivated.connect(self.close)

        login_container.addStretch()
        login_container.addWidget(login_text)
        login_container.addSpacing(5)
        login_container.addWidget(login_link)
        login_container.addStretch()

        signup_layout.addSpacing(10)
        signup_layout.addLayout(login_container)

        # Set scroll area widget
        scroll_area.setWidget(signup_frame)

        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)

    def get_input_style(self):
        return """
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
                color: #333;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #f0b03f;
                background-color: white;
            }
        """

    def validate_username(self, text):
        """Validate username - no spaces allowed"""
        if ' ' in text:
            cursor_pos = self.username_input.cursorPosition()
            self.username_input.setText(text.replace(' ', ''))
            self.username_input.setCursorPosition(cursor_pos - 1)

    def validate_phone(self, text):
        """Visual feedback for phone number validation"""
        if len(text) == 11:
            self.phone_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px 15px;
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    background-color: #fafafa;
                    color: #333;
                    font-size: 12px;
                }
            """)
        else:
            self.phone_input.setStyleSheet(self.get_input_style())

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_toggle.setText('hide')
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_toggle.setText('show')

    def toggle_confirm_password_visibility(self):
        """Toggle confirm password visibility"""
        self.confirm_password_visible = not self.confirm_password_visible
        if self.confirm_password_visible:
            self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_password_toggle.setText('hide')
        else:
            self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_password_toggle.setText('show')

    def handle_signup(self):
        firstname = self.firstname_input.text().strip()
        middlename = self.middlename_input.text().strip()
        lastname = self.lastname_input.text().strip()
        username = self.username_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validation - all fields except middle name are required
        if not all([firstname, lastname, username, phone, password, confirm_password]):
            self.show_styled_warning('Error', 'Please fill in all required fields marked with *!')
            return

        # Validate username - no spaces
        if ' ' in username:
            self.show_styled_warning('Error', 'Username cannot contain spaces!')
            return

        # Validate phone number - exactly 11 digits
        if not phone.isdigit():
            self.show_styled_warning('Error', 'Phone number must contain only digits!')
            return

        if len(phone) != 11:
            self.show_styled_warning('Error', 'Phone number must be exactly 11 digits!')
            return

        # Validate password
        if password != confirm_password:
            self.show_styled_warning('Error', 'Passwords do not match!')
            return

        if len(password) < 6:
            self.show_styled_warning('Error', 'Password must be at least 6 characters!')
            return

        # Check if database manager is available
        if not self.db_manager or not self.db_manager.connection:
            self.show_styled_warning('Error', 'Database connection not available!')
            return

        # Register user in database
        success, message = self.db_manager.register_user(
            username=username,
            password=password,
            first_name=firstname,
            middle_name=middlename if middlename else None,
            last_name=lastname,
            phone_number=phone
        )

        if success:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Success')
            msg_box.setText(message)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #ffffff;
                }
                QLabel {
                    color: #000000;  
                    font-size: 12px;
                    min-width: 300px;
                }
                QPushButton {
                    background-color: #f0b03f;
                    color: #000000;
                    padding: 8px 20px;
                    border-radius: 5px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #ffc14d;
                }
            """)
            msg_box.exec()
            self.accept()
        else:
            self.show_styled_warning('Registration Failed', message)

    def show_styled_warning(self, title, message):
        """Simple helper for styled error messages"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet(
            "QMessageBox QLabel { color: #000000; } QPushButton { background-color: #f0b03f; color: #000000; padding: 5px 15px; }")
        msg.exec()