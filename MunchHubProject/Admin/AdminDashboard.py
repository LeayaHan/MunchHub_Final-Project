from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Admin.AdminController import AdminController
from datetime import datetime
import sys
import os


class AdminDashboard(QMainWindow):
    def __init__(self, admin_data, db_manager):
        super().__init__()
        self.admin_data = admin_data
        self.db_manager = db_manager
        self.controller = AdminController(db_manager)
        self.current_page = "Dashboard"
        self.initUI()
        self.load_dashboard_data()

    def initUI(self):
        self.setWindowTitle('MunchHub - Admin Dashboard')
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("background-color: #f5f5f5;")

        # Set window icon
        self.set_window_icon()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        self.content_container = QWidget()
        main_layout.addWidget(self.content_container)

        self.show_dashboard()

    def set_window_icon(self):
        """Set the window icon from PNG/logo.png"""
        try:
            # Get the path to logo.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            logo_path = os.path.join(parent_dir, 'PNG', 'logo.png')

            if os.path.exists(logo_path):
                self.setWindowIcon(QIcon(logo_path))
            else:
                print(f"Logo not found at: {logo_path}")
        except Exception as e:
            print(f"Error setting window icon: {e}")

    def create_sidebar(self):
        """Create sidebar with navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #003274;
                border-right: 2px solid #002050;
            }
        """)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar.setLayout(sidebar_layout)

        # Header
        header = self.create_sidebar_header()
        sidebar_layout.addWidget(header)

        # Navigation
        nav_container = self.create_navigation()
        sidebar_layout.addWidget(nav_container)

        return sidebar

    def create_sidebar_header(self):
        """Create sidebar header with logo"""
        header = QFrame()
        header.setFixedHeight(200)
        header.setStyleSheet("background-color: #003274; border: none;")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(10)
        header.setLayout(header_layout)

        # Logo image
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            # Get the path to logo.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            logo_path = os.path.join(parent_dir, 'PNG', 'logo.png')

            if os.path.exists(logo_path):
                pixmap = QPixmap(logo_path)
                # Scale the logo to fit nicely in the sidebar (adjust size as needed)
                scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                # Fallback text if logo not found
                logo_label.setText("ADMIN")
                logo_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
                logo_label.setStyleSheet("color: white;")
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback text
            logo_label.setText("ADMIN")
            logo_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
            logo_label.setStyleSheet("color: white;")

        header_layout.addWidget(logo_label)

        admin_name = QLabel(self.admin_data['full_name'])
        admin_name.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        admin_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        admin_name.setStyleSheet("color: white;")
        header_layout.addWidget(admin_name)

        role_label = QLabel("Administrator")
        role_label.setFont(QFont('Arial', 9))
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_label.setStyleSheet("color: white;")
        header_layout.addWidget(role_label)

        return header

    def create_navigation(self):
        """Create navigation menu"""
        nav_container = QWidget()
        nav_container.setStyleSheet("background-color: #003274;")
        nav_layout = QVBoxLayout()
        nav_layout.setContentsMargins(10, 20, 10, 10)
        nav_layout.setSpacing(5)
        nav_container.setLayout(nav_layout)

        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Activity Log", self.show_activity_log),
            ("Manage Menu", self.show_manage_menu),
            ("Manage Staff", self.show_manage_staff),
            ("Reports", self.show_reports)
        ]

        self.nav_buttons = []
        for text, callback in nav_items:
            btn = self.create_nav_button(text, callback)
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        if self.nav_buttons:
            self.set_active_button(self.nav_buttons[0])

        nav_layout.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont('Arial', 11))
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setMinimumHeight(45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd59;
                color: black;
                border: none;
                border-radius: 8px;
                padding: 10px;
                text-align: left;
                padding-left: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f44336;
                color: white;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        nav_layout.addWidget(logout_btn)

        return nav_container

    def create_nav_button(self, text, callback):
        """Create a navigation button"""
        btn = QPushButton(text)
        btn.setFont(QFont('Arial', 11))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        btn.clicked.connect(lambda: [self.set_active_button(btn), callback()])
        return btn

    def set_active_button(self, active_btn):
        """Set active state for navigation button"""
        for btn in self.nav_buttons:
            if btn == active_btn:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #002050;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        text-align: left;
                        padding-left: 20px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.2);
                    }
                """)

    def clear_content(self):
        """Clear current content"""
        if self.content_container.layout():
            QWidget().setLayout(self.content_container.layout())
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.content_container.setLayout(layout)
        return layout

    def show_dashboard(self):
        """Show dashboard with clean minimal stats cards and date filtering"""
        self.current_page = "Dashboard"
        layout = self.clear_content()

        # Title and Filter Row
        title_filter_layout = QHBoxLayout()

        title_label = QLabel("Dashboard Overview")
        title_label.setFont(QFont('Arial', 32, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #003274; margin-bottom: 30px;")
        title_filter_layout.addWidget(title_label)

        title_filter_layout.addStretch()

        # Filter Controls Container
        filter_container = QWidget()
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setSpacing(15)  # Increased spacing from 10 to 15
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_container.setLayout(self.filter_layout)

        # Filter Type Dropdown
        filter_label = QLabel("Filter by:")
        filter_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        filter_label.setStyleSheet("color: #003274; font-weight: bold;")
        self.filter_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Time", "Year", "Month", "Day"])
        self.filter_combo.setFont(QFont('Arial', 11))
        self.filter_combo.setMinimumWidth(120)
        self.filter_combo.setMaxVisibleItems(10)  # Enable scrolling
        self.filter_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 2px solid #003274;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
            QComboBox:hover {
                border: 2px solid #0052a3;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #003274;
                background-color: white;
                selection-background-color: #003274;
                selection-color: white;
            }
        """)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        self.filter_layout.addWidget(self.filter_combo)

        # Year Selector
        self.year_combo = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 1):
            self.year_combo.addItem(str(year))
        self.year_combo.setCurrentText(str(current_year))
        self.year_combo.setFont(QFont('Arial', 11))
        self.year_combo.setMinimumWidth(100)
        self.year_combo.setMaxVisibleItems(10)  # Enable scrolling
        self.year_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.year_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 2px solid #003274;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
            QComboBox:hover {
                border: 2px solid #0052a3;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #003274;
                background-color: white;
                selection-background-color: #003274;
                selection-color: white;
            }
        """)
        self.year_combo.setVisible(False)
        self.year_combo.currentTextChanged.connect(self.refresh_dashboard_data)
        self.filter_layout.addWidget(self.year_combo)

        # Month Selector
        self.month_combo = QComboBox()
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        for i, month in enumerate(months, 1):
            self.month_combo.addItem(month, i)
        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        self.month_combo.setFont(QFont('Arial', 11))
        self.month_combo.setMinimumWidth(120)
        self.month_combo.setMaxVisibleItems(10)  # Enable scrolling
        self.month_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.month_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 2px solid #003274;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
            QComboBox:hover {
                border: 2px solid #0052a3;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #003274;
                background-color: white;
                selection-background-color: #003274;
                selection-color: white;
            }
        """)
        self.month_combo.setVisible(False)
        self.month_combo.currentTextChanged.connect(self.refresh_dashboard_data)
        self.filter_layout.addWidget(self.month_combo)

        # Day Selector
        self.day_combo = QComboBox()
        for day in range(1, 32):
            self.day_combo.addItem(str(day))
        self.day_combo.setCurrentIndex(datetime.now().day - 1)
        self.day_combo.setFont(QFont('Arial', 11))
        self.day_combo.setMinimumWidth(80)
        self.day_combo.setMaxVisibleItems(10)  # Enable scrolling
        self.day_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.day_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 2px solid #003274;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
            QComboBox:hover {
                border: 2px solid #0052a3;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #003274;
                background-color: white;
                selection-background-color: #003274;
                selection-color: white;
            }
        """)
        self.day_combo.setVisible(False)
        self.day_combo.currentTextChanged.connect(self.refresh_dashboard_data)
        self.filter_layout.addWidget(self.day_combo)

        title_filter_layout.addWidget(filter_container)
        layout.addLayout(title_filter_layout)

        # Stats Container (will be populated by refresh_dashboard_data)
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout()
        self.stats_layout.setSpacing(20)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_container.setLayout(self.stats_layout)
        layout.addWidget(self.stats_container)

        layout.addStretch()

        # Load initial data
        self.refresh_dashboard_data()

    def on_filter_changed(self, filter_type):
        """Handle filter type change"""
        self.year_combo.setVisible(filter_type in ["Year", "Month", "Day"])
        self.month_combo.setVisible(filter_type in ["Month", "Day"])
        self.day_combo.setVisible(filter_type == "Day")

        # Adjust spacing based on filter type
        if filter_type == "Day":
            self.filter_layout.setSpacing(10)  # Reduced spacing when Day filter is active
        else:
            self.filter_layout.setSpacing(15)  # Normal spacing for other filters

        self.refresh_dashboard_data()

    def refresh_dashboard_data(self):
        """Refresh dashboard with current filter settings"""
        # Get filter parameters
        filter_type = self.filter_combo.currentText().lower().replace(" ", "")
        year = int(self.year_combo.currentText()) if self.year_combo.isVisible() else None
        month = self.month_combo.currentData() if self.month_combo.isVisible() else None
        day = int(self.day_combo.currentText()) if self.day_combo.isVisible() else None

        # Get filtered stats
        stats_data = self.controller.get_dashboard_stats(filter_type, year, month, day)

        # Clear existing stats
        while self.stats_layout.count():
            child = self.stats_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

        # Top row stats
        top_stats_label = QLabel("Key Metrics")
        top_stats_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        top_stats_label.setStyleSheet("color: #000000; margin-top: 10px; margin-bottom: 15px;")
        self.stats_layout.addWidget(top_stats_label)

        top_stats_container = QHBoxLayout()
        top_stats_container.setSpacing(25)

        top_stats = [
            ("Total Users", str(stats_data['total_users']), "#4CAF50"),
            ("Total Orders", str(stats_data['total_orders']), "#2196F3"),
            ("Menu Items", str(stats_data['total_menu_items']), "#9C27B0")
        ]

        for title, value, color in top_stats:
            card = self.create_minimal_stat_card(title, value, color)
            top_stats_container.addWidget(card)

        self.stats_layout.addLayout(top_stats_container)

        # Revenue breakdown
        revenue_label = QLabel("Revenue Breakdown")
        revenue_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        revenue_label.setStyleSheet("color: #000000; margin-top: 30px; margin-bottom: 15px;")
        self.stats_layout.addWidget(revenue_label)

        revenue_container = QHBoxLayout()
        revenue_container.setSpacing(25)

        revenue_stats = [
            ("Completed Revenue", f"₱{stats_data['total_revenue']:,.2f}", "#4CAF50"),
            ("Confirmed Revenue", f"₱{stats_data['confirmed_revenue']:,.2f}", "#FF9800"),
            ("Pending Orders", f"{stats_data['total_pending_orders']}", "#F44336")
        ]

        for title, value, color in revenue_stats:
            card = self.create_minimal_stat_card(title, value, color)
            revenue_container.addWidget(card)

        self.stats_layout.addLayout(revenue_container)

        # Info note
        info_note = QLabel(
            "Note: Completed = Delivered orders only | "
            "Confirmed = Accepted + Out for delivery + Delivered | "
            "Pending = Awaiting staff confirmation"
        )
        info_note.setFont(QFont('Arial', 10))
        info_note.setStyleSheet("""
            color: #555; 
            padding: 15px; 
            background-color: #f0f0f0; 
            border-radius: 5px;
            margin-top: 20px;
        """)
        info_note.setWordWrap(True)
        self.stats_layout.addWidget(info_note)

    def clear_layout(self, layout):
        """Helper to clear a layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def create_minimal_stat_card(self, title, value, color):
        """Create minimal clean stat card with just number and label"""
        card = QFrame()
        card.setMinimumHeight(150)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)

        # Subtle shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 20))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        card.setLayout(layout)

        layout.addStretch()

        # Value - Large number (reduced font size to fit longer numbers)
        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setWordWrap(True)
        layout.addWidget(value_label)

        # Title - Label below
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 13))
        title_label.setStyleSheet("color: #666;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        layout.addStretch()

        return card

    def show_activity_log(self):
        """Show activity log page"""
        from Admin.ActivityLogView import ActivityLogView
        self.current_page = "Activity Log"
        layout = self.clear_content()

        activity_view = ActivityLogView(self.controller, self)
        layout.addWidget(activity_view)

    def show_manage_menu(self):
        """Show manage menu page"""
        from Admin.MenuManagementView import MenuManagementView
        self.current_page = "Manage Menu"
        layout = self.clear_content()

        menu_view = MenuManagementView(self.controller, self)
        layout.addWidget(menu_view)

    def show_manage_staff(self):
        """Show manage staff page"""
        from Admin.StaffManagementView import StaffManagementView
        self.current_page = "Manage Staff"
        layout = self.clear_content()

        staff_view = StaffManagementView(self.controller, self)
        layout.addWidget(staff_view)

    def show_reports(self):
        """Show reports page"""
        from Admin.ReportsView import ReportsView
        self.current_page = "Reports"
        layout = self.clear_content()

        reports_view = ReportsView(self.controller, self)
        layout.addWidget(reports_view)

    def load_dashboard_data(self):
        """Load initial dashboard data"""
        pass

    def handle_logout(self):
        """Handle logout and return to login window"""
        # Apply message box styling for visibility
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

        reply = QMessageBox.question(
            self,
            'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Get the current file's directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)

                # Add necessary paths
                paths_to_add = [
                    parent_dir,
                    os.path.join(parent_dir, 'Main'),
                    current_dir
                ]

                for path in paths_to_add:
                    if path not in sys.path:
                        sys.path.insert(0, path)

                # Try importing LoginWindow with multiple strategies
                LoginWindow = None

                # Strategy 1: From Main folder
                try:
                    from Main.LoginWindow import LoginWindow
                except ImportError:
                    pass

                # Strategy 2: Direct import
                if LoginWindow is None:
                    try:
                        from LoginWindow import LoginWindow
                    except ImportError:
                        pass

                # If import failed, show error and close
                if LoginWindow is None:
                    QMessageBox.warning(
                        self,
                        'Logout',
                        'Logged out successfully.\n\nPlease restart the application to login again.'
                    )
                    self.close()
                    return

                # Create and show login window
                self.login_window = LoginWindow(self.db_manager)
                self.login_window.show()

                # Close admin dashboard
                self.close()

            except Exception as e:
                # If anything goes wrong, still close the admin dashboard
                print(f"Error during logout: {e}")
                import traceback
                traceback.print_exc()

                QMessageBox.information(
                    self,
                    'Logout',
                    'Logged out successfully.\n\nPlease restart the application to login again.'
                )
                self.close()