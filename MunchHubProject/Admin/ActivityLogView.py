"""
ActivityLogView.py - Admin Activity Log View (Fixed)
Place this file in: Admin/ActivityLogView.py
Shows all staff activities from StaffActivityLog table
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Admin.AdminComponents import StyledTable


class ActivityLogView(QWidget):
    """Activity Log View - Shows all staff activities"""

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

        title_label = QLabel("Staff Activity Log")
        title_label.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

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
        refresh_btn.clicked.connect(self.load_activity_logs)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Info label
        info_label = QLabel("View all staff activities and order management actions")
        info_label.setFont(QFont('Arial', 11))
        info_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(info_label)

        # Search and filter section
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by staff name, customer, order ID...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                color: black;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        self.search_input.textChanged.connect(self.filter_logs)
        filter_layout.addWidget(self.search_input)

        layout.addLayout(filter_layout)

        # Activity table
        self.activity_table = self.create_activity_table()
        layout.addWidget(self.activity_table)

        # Load initial data
        self.load_activity_logs()

    def create_activity_table(self):
        """Create activity log table"""
        table = StyledTable()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Staff ID",
            "Staff Name",
            "Order ID",
            "Customer",
            "Action",
            "Status",
            "Date & Time"
        ])

        # Disable table selection and focus
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Set column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        # Ensure word wrap is enabled for better visibility
        table.setWordWrap(True)
        table.setTextElideMode(Qt.TextElideMode.ElideNone)
        table.verticalHeader().setDefaultSectionSize(60)

        return table

    def load_activity_logs(self):
        """Load activity logs from StaffActivityLog table"""
        try:
            # Get logs from database using the controller method
            logs = self.get_staff_activity_logs_from_db()

            # Clear table first
            self.activity_table.setRowCount(0)

            if not logs:
                # Show empty message
                self.activity_table.setRowCount(1)
                no_data_item = QTableWidgetItem("No staff activity logs found")
                no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                no_data_item.setForeground(QColor('#999'))
                no_data_item.setFont(QFont('Arial', 12))
                # Disable item selection
                no_data_item.setFlags(no_data_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(0, 0, no_data_item)
                self.activity_table.setSpan(0, 0, 1, 7)
                return

            for log in logs:
                row = self.activity_table.rowCount()
                self.activity_table.insertRow(row)

                # Staff ID
                staff_id = str(log.get('StaffID', 'N/A'))
                staff_id_item = QTableWidgetItem(staff_id)
                staff_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                staff_id_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
                staff_id_item.setForeground(QColor('#003274'))
                # Disable item selection
                staff_id_item.setFlags(staff_id_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 0, staff_id_item)

                # Staff Name
                staff_name = str(log.get('StaffName', 'Unknown Staff'))
                staff_name_item = QTableWidgetItem(staff_name)
                staff_name_item.setFont(QFont('Arial', 11))
                staff_name_item.setForeground(QColor('black'))
                # Disable item selection
                staff_name_item.setFlags(staff_name_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 1, staff_name_item)

                # Order ID
                order_id = str(log.get('OrderID', 'N/A'))
                order_id_item = QTableWidgetItem(order_id)
                order_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                order_id_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
                order_id_item.setForeground(QColor('#003274'))
                # Disable item selection
                order_id_item.setFlags(order_id_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 2, order_id_item)

                # Customer
                customer = str(log.get('CustomerName', 'Unknown Customer'))
                customer_item = QTableWidgetItem(customer)
                customer_item.setFont(QFont('Arial', 11))
                customer_item.setForeground(QColor('black'))
                # Disable item selection
                customer_item.setFlags(customer_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 3, customer_item)

                # Action
                action = str(log.get('Action', 'Unknown Action'))
                action_item = QTableWidgetItem(action)
                action_item.setFont(QFont('Arial', 11))
                action_item.setForeground(QColor('black'))
                # Disable item selection
                action_item.setFlags(action_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 4, action_item)

                # Status - Color coded
                status = str(log.get('Status', 'Unknown'))
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                status_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))

                # Color code by status
                status_colors = {
                    'Pending': '#FF9800',
                    'Preparing': '#2196F3',
                    'Out for delivery': '#9C27B0',
                    'Delivered': '#4CAF50',
                    'Cancelled': '#F44336'
                }
                color = status_colors.get(status, '#757575')
                status_item.setForeground(QColor(color))
                # Disable item selection
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 5, status_item)

                # Timestamp
                timestamp = log.get('ActivityDate', 'N/A')
                if timestamp != 'N/A':
                    # Format timestamp if it's a datetime object
                    if hasattr(timestamp, 'strftime'):
                        timestamp = timestamp.strftime('%b %d, %Y %I:%M %p')
                    else:
                        timestamp = str(timestamp)

                timestamp_item = QTableWidgetItem(timestamp)
                timestamp_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                timestamp_item.setFont(QFont('Arial', 10))
                timestamp_item.setForeground(QColor('black'))
                # Disable item selection
                timestamp_item.setFlags(timestamp_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.activity_table.setItem(row, 6, timestamp_item)

            # Show count
            print(f"Loaded {len(logs)} staff activity log entries")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading activity logs: {str(e)}")
            import traceback
            traceback.print_exc()

    def get_staff_activity_logs_from_db(self):
        """Get staff activity logs directly from StaffActivityLog table"""
        try:
            cursor = self.controller.db.connection.cursor(dictionary=True)

            # Query StaffActivityLog table with proper joins
            query = """
                SELECT 
                    sal.LogID,
                    sal.StaffID,
                    CONCAT(COALESCE(su.UFirstName, ''), ' ', COALESCE(su.ULastName, '')) as StaffName,
                    sal.OrderID,
                    sal.CustomerID,
                    CONCAT(COALESCE(cu.UFirstName, ''), ' ', COALESCE(cu.ULastName, '')) as CustomerName,
                    sal.Action,
                    sal.Status,
                    sal.ActivityDate
                FROM StaffActivityLog sal
                LEFT JOIN Staffs s ON sal.StaffID = s.StaffID
                LEFT JOIN Users su ON s.UserID = su.UserID
                LEFT JOIN Customers c ON sal.CustomerID = c.CustomerID
                LEFT JOIN Users cu ON c.UserID = cu.UserID
                ORDER BY sal.ActivityDate DESC
                LIMIT 100
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Clean up any missing data
            for result in results:
                if not result.get('StaffName') or result['StaffName'].strip() == '':
                    result['StaffName'] = f"Staff {result.get('StaffID', 'Unknown')}"
                if not result.get('CustomerName') or result['CustomerName'].strip() == '':
                    result['CustomerName'] = f"Customer {result.get('CustomerID', 'Unknown')}"
                if not result.get('Action'):
                    result['Action'] = 'Unknown Action'
                if not result.get('Status'):
                    result['Status'] = 'Unknown'
                if not result.get('OrderID'):
                    result['OrderID'] = 'N/A'

            return results

        except Exception as e:
            print(f"Error getting staff activity logs: {e}")
            import traceback
            traceback.print_exc()
            return []

    def filter_logs(self, search_text):
        """Filter activity logs by search text"""
        for row in range(self.activity_table.rowCount()):
            match = False
            for col in range(7):  # Search in all columns
                item = self.activity_table.item(row, col)
                if item and search_text.lower() in item.text().lower():
                    match = True
                    break
            self.activity_table.setRowHidden(row, not match)