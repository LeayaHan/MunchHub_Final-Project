"""
StaffDashboard.py - Main Staff Dashboard (View)
Place this file in: Staff/StaffDashboard.py
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Staff.StaffController import StaffController
from Staff.ManageOrdersPage import ManageOrdersPage
from Staff.ActivityLogPage import ActivityLogPage
from Staff.TrackOrdersPage import TrackOrdersPage


class StaffDashboard(QMainWindow):
    """Main dashboard for staff members"""

    def __init__(self, staff_data, db_manager):
        super().__init__()
        self.staff_data = staff_data
        self.db_manager = db_manager
        self.controller = StaffController(db_manager, staff_data)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MunchHub - Staff Dashboard')
        self.setMinimumSize(1200, 700)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #f5f5f5;")

        # Add pages
        self.manage_orders_page = ManageOrdersPage(self.controller, self)
        self.activity_log_page = ActivityLogPage(self.controller, self)
        self.track_orders_page = TrackOrdersPage(self.controller, self)

        self.content_stack.addWidget(self.manage_orders_page)
        self.content_stack.addWidget(self.activity_log_page)
        self.content_stack.addWidget(self.track_orders_page)

        main_layout.addWidget(self.content_stack, 1)

        # Load initial page
        self.manage_orders_page.load_data()

    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #003274, stop:1 #004a9e);
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header_widget = self.create_header()
        layout.addWidget(header_widget)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: rgba(255,255,255,0.2); margin: 0 20px;")
        layout.addWidget(divider)

        # Navigation buttons
        nav_widget = QWidget()
        nav_widget.setStyleSheet("background: transparent;")
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(20, 20, 20, 20)
        nav_layout.setSpacing(10)

        self.manage_orders_btn = self.create_nav_button("Manage Orders", True)
        self.manage_orders_btn.clicked.connect(lambda: self.switch_page(0, self.manage_orders_btn))
        nav_layout.addWidget(self.manage_orders_btn)

        self.activity_log_btn = self.create_nav_button("My Activity Log", False)
        self.activity_log_btn.clicked.connect(lambda: self.switch_page(1, self.activity_log_btn))
        nav_layout.addWidget(self.activity_log_btn)

        self.track_orders_btn = self.create_nav_button("Track Orders", False)
        self.track_orders_btn.clicked.connect(lambda: self.switch_page(2, self.track_orders_btn))
        nav_layout.addWidget(self.track_orders_btn)

        layout.addWidget(nav_widget)
        layout.addStretch()

        # Logout button
        logout_container = self.create_logout_button()
        layout.addWidget(logout_container)

        return sidebar

    def create_header(self):
        """Create sidebar header"""
        header_widget = QWidget()
        header_widget.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 30, 20, 30)
        header_layout.setSpacing(10)

        # Logo image
        logo_label = QLabel()
        logo_pixmap = QPixmap("PNG/logo.png")
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback if image not found
            logo_label.setText("MH")
            logo_label.setFont(QFont('Arial', 48, QFont.Weight.Bold))
            logo_label.setStyleSheet("color: white;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        title = QLabel("MunchHub")
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)

        staff_name = QLabel(f"{self.staff_data['full_name']}")
        staff_name.setFont(QFont('Arial', 11))
        staff_name.setStyleSheet("color: rgba(255,255,255,0.8);")
        staff_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        staff_name.setWordWrap(True)
        header_layout.addWidget(staff_name)

        staff_id = QLabel(f"ID: {self.staff_data['staff_id']}")
        staff_id.setFont(QFont('Arial', 10))
        staff_id.setStyleSheet("color: rgba(255,255,255,0.6);")
        staff_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(staff_id)

        return header_widget

    def create_nav_button(self, text, active=False):
        """Create navigation button"""
        btn = QPushButton(text)
        btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(50)

        if active:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 189, 89, 0.9);
                    color: #003274;
                    border: none;
                    border-radius: 8px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 189, 89, 1);
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: 2px solid rgba(255,255,255,0.2);
                    border-radius: 8px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.1);
                    border: 2px solid rgba(255,255,255,0.4);
                }
            """)

        return btn

    def create_logout_button(self):
        """Create logout button container"""
        logout_container = QWidget()
        logout_container.setStyleSheet("background: transparent;")
        logout_layout = QVBoxLayout(logout_container)
        logout_layout.setContentsMargins(20, 20, 20, 30)

        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setFixedHeight(50)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(244, 67, 54, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(211, 47, 47, 0.9);
            }
        """)
        logout_btn.clicked.connect(self.logout)
        logout_layout.addWidget(logout_btn)

        return logout_container

    def switch_page(self, index, button):
        """Switch between pages"""
        # Reset all buttons
        for btn in [self.manage_orders_btn, self.activity_log_btn, self.track_orders_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: 2px solid rgba(255,255,255,0.2);
                    border-radius: 8px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.1);
                    border: 2px solid rgba(255,255,255,0.4);
                }
            """)

        # Set active button
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 189, 89, 0.9);
                color: #003274;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 189, 89, 1);
            }
        """)

        # Switch page and load data
        self.content_stack.setCurrentIndex(index)

        if index == 0:
            self.manage_orders_page.load_data()
        elif index == 1:
            self.activity_log_page.load_data()
        elif index == 2:
            self.track_orders_page.load_data()

    def logout(self):
        """Logout"""
        reply = QMessageBox.question(
            self,
            'Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            from Main.LoginWindow import LoginWindow
            self.login_window = LoginWindow(self.db_manager)
            self.login_window.show()
            self.close()