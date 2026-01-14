"""
ActivityLogPage.py - Activity Log Page with delivery confirmation
Place this file in: Staff/ActivityLogPage.py
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class ActivityLogPage(QWidget):
    """Page for viewing staff activity log with delivery confirmation"""

    def __init__(self, controller, parent):
        super().__init__(parent)
        self.controller = controller
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = self.create_header()
        layout.addLayout(header_layout)

        # Info banner about delivery confirmation
        info_banner = QLabel(
            "Tip: For orders marked as 'Delivered' in the activity log, "
            "you can verify if the customer confirmed receipt by checking the Order Track page"
        )
        info_banner.setFont(QFont('Arial', 10))
        info_banner.setStyleSheet("""
            color: #555;
            background-color: #fff3e0;
            padding: 12px;
            border-left: 4px solid #FF9800;
            border-radius: 5px;
        """)
        info_banner.setWordWrap(True)
        layout.addWidget(info_banner)

        # Activity table
        self.activity_table = self.create_activity_table()
        layout.addWidget(self.activity_table)

    def create_header(self):
        """Create page header"""
        header_layout = QHBoxLayout()

        title = QLabel("My Activity Log")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setFixedSize(120, 40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(refresh_btn)

        return header_layout

    def create_activity_table(self):
        """Create activity table"""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Order ID", "Customer", "Action", "Status", "Date & Time", "Details", "Actions"
        ])

        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                color: black;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #003274;
                color: white;
                padding: 12px;
                font-weight: bold;
                border: none;
            }
        """)

        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # MODIFIED: Disable table selection and focus
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(65)

        return table

    def load_data(self):
        """Load activity log"""
        activities = self.controller.get_activity_log()
        self.populate_table(activities)

    def populate_table(self, activities):
        """Populate table with activities"""
        self.activity_table.setRowCount(len(activities) if activities else 1)

        if not activities:
            empty_msg = QTableWidgetItem("No activity records found")
            empty_msg.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_msg.setForeground(QColor('#999'))
            # MODIFIED: Disable item selection
            empty_msg.setFlags(empty_msg.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.activity_table.setItem(0, 0, empty_msg)
            self.activity_table.setSpan(0, 0, 1, 7)
            return

        status_colors = {
            'Pending': '#FF9800',
            'Preparing': '#2196F3',
            'Out for delivery': '#9C27B0',
            'Delivered': '#4CAF50',
            'Cancelled': '#F44336'
        }

        for row, activity in enumerate(activities):
            # Order ID
            order_item = QTableWidgetItem(activity['OrderID'])
            order_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            order_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            order_item.setForeground(QColor('#003274'))
            # MODIFIED: Disable item selection
            order_item.setFlags(order_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.activity_table.setItem(row, 0, order_item)

            # Customer
            customer_item = QTableWidgetItem(activity['CustomerName'])
            customer_item.setForeground(QColor('black'))
            # MODIFIED: Disable item selection
            customer_item.setFlags(customer_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.activity_table.setItem(row, 1, customer_item)

            # Action
            action_item = QTableWidgetItem(activity['Action'])
            action_item.setForeground(QColor('black'))
            # MODIFIED: Disable item selection
            action_item.setFlags(action_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.activity_table.setItem(row, 2, action_item)

            # Status
            status_item = QTableWidgetItem(activity['Status'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            status_item.setForeground(QColor(status_colors.get(activity['Status'], '#666')))
            # MODIFIED: Disable item selection
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.activity_table.setItem(row, 3, status_item)

            # Date & Time
            date_str = activity['ActivityDate'].strftime('%b %d, %Y %I:%M %p')
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setForeground(QColor('black'))
            # MODIFIED: Disable item selection
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.activity_table.setItem(row, 4, date_item)

            # Details button
            details_widget = self.create_details_button(activity)
            self.activity_table.setCellWidget(row, 5, details_widget)

            # Action buttons (Mark as Delivered if status is Out for delivery)
            if activity['Status'] == 'Out for delivery':
                action_widget = self.create_action_button(activity)
                self.activity_table.setCellWidget(row, 6, action_widget)
            else:
                # Show status indicator
                status_widget = self.create_status_indicator(activity['Status'])
                self.activity_table.setCellWidget(row, 6, status_widget)

    def create_details_button(self, activity):
        """Create details button"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        details_btn = QPushButton("View")
        details_btn.setFixedSize(80, 30)
        details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        details_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        details_btn.clicked.connect(lambda: self.view_details(activity))

        layout.addWidget(details_btn)

        return widget

    def create_action_button(self, activity):
        """Create action button for orders out for delivery"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        deliver_btn = QPushButton("Delivered")
        deliver_btn.setFixedSize(100, 30)
        deliver_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        deliver_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        deliver_btn.clicked.connect(lambda: self.mark_as_delivered(activity))

        layout.addWidget(deliver_btn)

        return widget

    def create_status_indicator(self, status):
        """Create status indicator for completed/cancelled orders"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if status == 'Delivered':
            indicator = QLabel("Complete")
            indicator.setStyleSheet("""
                color: #4CAF50;
                font-weight: bold;
                font-size: 10px;
            """)
        elif status == 'Cancelled':
            indicator = QLabel("Cancelled")
            indicator.setStyleSheet("""
                color: #F44336;
                font-weight: bold;
                font-size: 10px;
            """)
        else:
            indicator = QLabel("—")
            indicator.setStyleSheet("color: #999;")

        layout.addWidget(indicator)

        return widget

    def mark_as_delivered(self, activity):
        """Mark order as delivered"""
        # Set message box styling for black text
        QApplication.instance().setStyleSheet("""
            QMessageBox QLabel { color: black; }
            QMessageBox QPushButton { 
                color: black;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)

        reply = QMessageBox.question(
            self,
            'Confirm Delivery',
            f"Mark Order #{activity['OrderID']} as delivered?\n\n"
            f"Customer: {activity['CustomerName']}\n\n"
            "This confirms that the customer has received their order.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.mark_order_delivered(activity['OrderID'])

            # Set message box styling for black text
            QApplication.instance().setStyleSheet("""
                QMessageBox QLabel { color: black; }
                QMessageBox QPushButton { 
                    color: black;
                    background-color: #e0e0e0;
                    border: 1px solid #ccc;
                    padding: 5px 15px;
                    border-radius: 4px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """)

            if success:
                QMessageBox.information(
                    self,
                    'Success',
                    f"Order #{activity['OrderID']} has been marked as delivered!\n\n"
                    "The order is now complete and will count towards sales revenue."
                )
                self.load_data()  # Refresh the table
            else:
                QMessageBox.critical(self, 'Error', message)

    def view_details(self, activity):
        """View activity details"""
        # Set message box styling for black text
        QApplication.instance().setStyleSheet("""
            QMessageBox QLabel { color: black; }
            QMessageBox QPushButton { 
                color: black;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)

        details_text = f"""
Order ID: {activity['OrderID']}
Customer: {activity['CustomerName']}
Action: {activity['Action']}
Status: {activity['Status']}
Date & Time: {activity['ActivityDate'].strftime('%B %d, %Y at %I:%M %p')}

Note: {'Orders marked as "Out for delivery" can be confirmed as delivered.' if activity['Status'] == 'Out for delivery' else 'This order has been processed.'}
        """
        QMessageBox.information(self, 'Activity Details', details_text.strip())