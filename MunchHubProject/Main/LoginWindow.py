import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add parent directory to Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import Customer Dashboard with multiple fallback options
CustomerWindow = None
try:
    from Customer.CustomerWindow import CustomerWindow

    print("✓ CustomerWindow imported from Customer.CustomerWindow")
except ImportError:
    try:
        # Try direct import from same directory
        sys.path.insert(0, current_dir)
        from CustomerWindow import CustomerWindow

        print("✓ CustomerWindow imported from current directory")
    except ImportError:
        try:
            # Try importing from Customer subfolder in current directory
            customer_path = os.path.join(current_dir, 'Customer')
            if customer_path not in sys.path:
                sys.path.insert(0, customer_path)
            from CustomerWindow import CustomerWindow

            print("✓ CustomerWindow imported from Customer subfolder")
        except ImportError:
            print("✗ CustomerWindow not found in any location")
            CustomerWindow = None


class LoginWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.password_visible = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MunchHub - Login')
        self.setFixedSize(450, 650)

        # Set window background color
        self.setStyleSheet("background-color: #ffbd59;")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)

        # Login container frame
        login_frame = QFrame()
        login_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
            }
        """)

        # Add shadow effect to login frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        login_frame.setGraphicsEffect(shadow)

        # Login frame layout
        login_layout = QVBoxLayout()
        login_layout.setContentsMargins(40, 40, 40, 40)
        login_layout.setSpacing(12)
        login_frame.setLayout(login_layout)

        # Logo label - centered and bigger
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedHeight(150)
        logo_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)

        # Load your logo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, 'PNG', 'logo.png')

        # Try different possible paths
        if not os.path.exists(logo_path):
            logo_path = os.path.join(script_dir, '..', 'PNG', 'logo.png')
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(script_dir), 'PNG', 'logo.png')

        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            # Scale logo to be bigger (150x150) and keep it centered
            scaled_pixmap = logo_pixmap.scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback if logo not found - bigger emoji
            logo_label.setText("🍔")
            logo_label.setFont(QFont('Arial', 60))
            logo_label.setStyleSheet("""
                QLabel {
                    background-color: #1a3a6b;
                    border-radius: 75px;
                    border: 4px solid #f0b03f;
                    color: white;
                    min-width: 150px;
                    max-width: 150px;
                    min-height: 150px;
                    max-height: 150px;
                }
            """)

        login_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add spacing after logo
        login_layout.addSpacing(15)

        # Title
        title_label = QLabel('MunchHub')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 26, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a3a6b;")
        title_label.setFixedHeight(40)
        login_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel('Food Ordering System')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont('Arial', 12))
        subtitle_label.setStyleSheet("color: #666;")
        subtitle_label.setFixedHeight(25)
        login_layout.addWidget(subtitle_label)

        # Add spacing after subtitle
        login_layout.addSpacing(20)

        # Username field
        username_label = QLabel('Username')
        username_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #1a3a6b;")
        username_label.setFixedHeight(20)
        login_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setFont(QFont('Arial', 11))
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet("""
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
        """)
        login_layout.addWidget(self.username_input)

        # Password field with toggle
        password_label = QLabel('Password')
        password_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #1a3a6b;")
        password_label.setFixedHeight(20)
        login_layout.addWidget(password_label)

        password_container = QHBoxLayout()
        password_container.setSpacing(0)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont('Arial', 11))
        self.password_input.setMinimumHeight(45)
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
        self.password_toggle.setFixedSize(45, 45)
        self.password_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.password_toggle.setStyleSheet("""
            QPushButton {
                background-color: #fafafa;
                border: 2px solid #e0e0e0;
                border-left: none;
                border-radius: 0px 8px 8px 0px;
                font-size: 16px;
                color: black;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.password_toggle.clicked.connect(self.toggle_password_visibility)

        password_container.addWidget(self.password_input)
        password_container.addWidget(self.password_toggle)
        login_layout.addLayout(password_container)

        # Login button
        login_button = QPushButton('Login')
        login_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.setMinimumHeight(50)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #1a3a6b;
                color: white;
                padding: 12px;
                border-radius: 8px;
                border: none;
                margin-top: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2d5a99;
            }
            QPushButton:pressed {
                background-color: #0f2847;
            }
        """)
        login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(login_button)

        # Sign up link
        signup_container = QHBoxLayout()
        signup_text = QLabel("Don't have an account?")
        signup_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        signup_text.setFont(QFont('Arial', 9))
        signup_text.setStyleSheet("color: #666;")

        signup_link = QLabel(
            '<a href="#" style="color: #f0b03f; text-decoration: none; font-weight: bold;">Sign Up</a>')
        signup_link.setAlignment(Qt.AlignmentFlag.AlignLeft)
        signup_link.setFont(QFont('Arial', 9))
        signup_link.setOpenExternalLinks(False)
        signup_link.linkActivated.connect(self.open_signup)

        signup_container.addStretch()
        signup_container.addWidget(signup_text)
        signup_container.addSpacing(5)
        signup_container.addWidget(signup_link)
        signup_container.addStretch()

        login_layout.addSpacing(15)
        login_layout.addLayout(signup_container)

        # Add login frame to main layout
        main_layout.addWidget(login_frame)

        # Enable Enter key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible

        self.password_toggle.setStyleSheet("color: #000000;")

        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_toggle.setText('hide')

        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_toggle.setText('show')

    def handle_login(self):
        """Handle login - automatically detects user type"""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Validation
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password!')
            return

        # Check for hardcoded admin account FIRST (no database needed)
        if username == 'admin' and password == 'admin123':
            # Create admin data without database
            self.admin_data = {
                'admin_id': 'A001',
                'username': 'admin',
                'full_name': 'System Administrator',
                'phone_number': '09123456789',
                'role': 'admin'
            }
            self.open_admin_dashboard()
            return

        # Check if database manager is available for regular users
        if not self.db_manager or not self.db_manager.connection:
            QMessageBox.critical(self, 'Error', 'Database connection not available!')
            return

        # Try to authenticate as admin from database (if admin table exists)
        admin_success, admin_data, admin_message = self.db_manager.authenticate_admin(username, password)

        if admin_success:
            self.admin_data = admin_data
            self.open_admin_dashboard()
            return

        # Try to authenticate as staff
        staff_success, staff_data, staff_message = self.db_manager.authenticate_staff(username, password)

        if staff_success:
            self.staff_data = staff_data
            self.open_staff_dashboard()
            return

        # Try to authenticate as regular user/customer
        user_success, user_data, user_message = self.db_manager.authenticate_user(username, password)

        if user_success:
            self.user_data = user_data
            self.open_customer_window()
            return

        # If all authentication attempts failed
        QMessageBox.warning(self, 'Login Failed', 'Invalid username or password!')
        self.password_input.clear()
        self.password_input.setFocus()

    def open_admin_dashboard(self):
        """Open admin dashboard window"""
        try:
            from Admin.AdminDashboard import AdminDashboard
            self.admin_window = AdminDashboard(self.admin_data, self.db_manager)
            self.admin_window.show()
            self.close()  # Changed from hide() to close()
        except ImportError as e:
            print(f"Error importing AdminDashboard: {e}")
            QMessageBox.warning(self, 'Error', 'Admin Dashboard not yet implemented!')

    def open_staff_dashboard(self):
        """Open staff dashboard window"""
        try:
            from Staff.StaffDashboard import StaffDashboard
            self.staff_window = StaffDashboard(self.staff_data, self.db_manager)
            self.staff_window.show()
            self.close()  # Changed from hide() to close()
        except ImportError as e:
            print(f"Error importing StaffDashboard: {e}")
            QMessageBox.warning(self, 'Error', 'Staff Dashboard not yet implemented!')

    def open_customer_window(self):
        """Open customer main window"""
        if CustomerWindow is None:
            QMessageBox.critical(
                self,
                'Error',
                'CustomerWindow.py not found!\n\n'
                'Please make sure CustomerWindow.py is in the Customer folder.'
            )
            return

        try:
            self.customer_window = CustomerWindow(self.user_data, self.db_manager)
            self.customer_window.show()
            self.close()
        except Exception as e:
            print(f"Error opening CustomerWindow: {e}")
            QMessageBox.critical(self, 'Error', f'Failed to open Customer Window: {str(e)}')

    def open_signup(self):
        """Open signup window"""
        try:
            from Main.SignUpWindow import SignUpWindow
            signup_dialog = SignUpWindow(self, self.db_manager)
            if signup_dialog.exec() == QDialog.DialogCode.Accepted:
                # No success message here - it's shown in SignUpWindow
                pass
        except ImportError as e:
            print(f"Error importing SignUpWindow: {e}")
            QMessageBox.warning(self, 'Error', 'Sign Up Window not yet implemented!')