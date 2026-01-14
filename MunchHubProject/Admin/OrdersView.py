from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Admin.AdminComponents import StyledTable, ActionButton


class OrdersView(QWidget):
    """Orders View - Manage customer orders"""

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

        title_label = QLabel("Orders Management")
        title_label.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
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
        refresh_btn.clicked.connect(self.load_orders)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Filter section
        filter_layout = QHBoxLayout()

        # Search input
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by Order ID or Customer...")
        search_input.setMinimumHeight(40)
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
            }
        """)
        search_input.textChanged.connect(self.filter_orders)
        filter_layout.addWidget(search_input)

        # Status filter
        status_combo = QComboBox()
        status_combo.setMinimumHeight(40)
        status_combo.addItem("All Statuses", "")
        status_combo.addItem("Pending", "Pending")
        status_combo.addItem("Preparing", "Preparing")
        status_combo.addItem("Out for Delivery", "Out for Delivery")
        status_combo.addItem("Delivered", "Delivered")
        status_combo.addItem("Cancelled", "Cancelled")
        status_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
            }
        """)
        status_combo.currentTextChanged.connect(lambda: self.filter_orders(search_input.text()))
        filter_layout.addWidget(status_combo)
        self.status_filter = status_combo

        layout.addLayout(filter_layout)

        # Orders table
        self.orders_table = self.create_orders_table()
        layout.addWidget(self.orders_table)

        # Load initial data
        self.load_orders()

    def create_orders_table(self):
        """Create orders table"""
        table = StyledTable()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Order ID", "Customer", "Total", "Delivery Fee", "Status", "Date", "Actions"
        ])

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        return table

    def load_orders(self):
        """Load orders from database"""
        try:
            orders = self.controller.get_all_orders()
            self.orders_table.setRowCount(len(orders))

            for row, order in enumerate(orders):
                # Order ID
                id_item = QTableWidgetItem(order['OrderID'])
                self.orders_table.setItem(row, 0, id_item)

                # Customer
                customer_name = f"{order['UFirstName']} {order['ULastName']}"
                customer_item = QTableWidgetItem(customer_name)
                self.orders_table.setItem(row, 1, customer_item)

                # Total
                total_item = QTableWidgetItem(f"₱{order['TotalFee']:.2f}")
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(row, 2, total_item)

                # Delivery Fee
                delivery_item = QTableWidgetItem(f"₱{order['DeliveryFee']:.2f}")
                delivery_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(row, 3, delivery_item)

                # Status
                status_item = QTableWidgetItem(order['OrderStatus'])
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Color code by status
                status_colors = {
                    'Pending': '#FF9800',
                    'Preparing': '#2196F3',
                    'Out for Delivery': '#9C27B0',
                    'Delivered': '#4CAF50',
                    'Cancelled': '#f44336'
                }
                color = status_colors.get(order['OrderStatus'], '#757575')
                status_item.setForeground(QColor(color))
                status_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
                self.orders_table.setItem(row, 4, status_item)

                # Date
                date_item = QTableWidgetItem(str(order['OrderDate']))
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(row, 5, date_item)

                # Actions - Create widget with buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(5, 5, 5, 5)
                actions_layout.setSpacing(5)
                actions_widget.setLayout(actions_layout)

                view_btn = QPushButton("👁️")
                view_btn.setToolTip("View Details")
                view_btn.setMaximumWidth(35)
                view_btn.setMinimumHeight(30)
                view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                view_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
                view_btn.clicked.connect(lambda checked, oid=order['OrderID']: self.view_order(oid))
                actions_layout.addWidget(view_btn)

                status_btn = QPushButton("📝")
                status_btn.setToolTip("Update Status")
                status_btn.setMaximumWidth(35)
                status_btn.setMinimumHeight(30)
                status_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                status_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                """)
                status_btn.clicked.connect(lambda checked, oid=order['OrderID'], r=row: self.update_status(oid, r))
                actions_layout.addWidget(status_btn)

                self.orders_table.setCellWidget(row, 6, actions_widget)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading orders: {e}")

    def filter_orders(self, search_text):
        """Filter orders by search text and status"""
        status_filter = self.status_filter.currentData()

        for row in range(self.orders_table.rowCount()):
            match_search = False
            match_status = True

            # Check search text
            for col in range(2):  # Search in Order ID and Customer
                item = self.orders_table.item(row, col)
                if item and search_text.lower() in item.text().lower():
                    match_search = True
                    break

            # Check status filter
            if status_filter:
                status_item = self.orders_table.item(row, 4)
                if status_item:
                    match_status = (status_item.text() == status_filter)

            # Show row only if both conditions match (or search is empty)
            show_row = (match_search or not search_text) and match_status
            self.orders_table.setRowHidden(row, not show_row)

    def view_order(self, order_id):
        """View order details"""
        dialog = OrderDetailsDialog(self.controller, order_id, parent=self)
        dialog.exec()

    def update_status(self, order_id, row):
        """Update order status"""
        current_status = self.orders_table.item(row, 4).text()

        dialog = StatusUpdateDialog(current_status, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_status = dialog.get_selected_status()
            if new_status != current_status:
                success, message = self.controller.update_order_status(order_id, new_status)
                if success:
                    QMessageBox.information(self, "Success", message)
                    self.load_orders()
                else:
                    QMessageBox.critical(self, "Error", message)


class OrderDetailsDialog(QDialog):
    """Dialog to view order details"""

    def __init__(self, controller, order_id, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.order_id = order_id
        self.initUI()
        self.load_order_details()

    def initUI(self):
        self.setWindowTitle(f"Order Details - {self.order_id}")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Title
        title = QLabel(f"Order #{self.order_id}")
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        layout.addWidget(title)

        # Details frame
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e6e6e6;
            }
        """)
        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(20, 20, 20, 20)
        details_layout.setSpacing(15)
        details_frame.setLayout(details_layout)

        self.details_label = QLabel()
        self.details_label.setFont(QFont('Arial', 12))
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet("color: #000000;")
        details_layout.addWidget(self.details_label)

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

    def load_order_details(self):
        """Load order details from database"""
        try:
            order = self.controller.get_order_details(self.order_id)
            if order:
                customer_name = f"{order['UFirstName']} {order['ULastName']}"
                details_text = f"""
                <p><strong>Customer:</strong> {customer_name}</p>
                <p><strong>Phone:</strong> {order['PhoneNum']}</p>
                <p><strong>Status:</strong> {order['OrderStatus']}</p>
                <p><strong>Total Fee:</strong> ₱{order['TotalFee']:.2f}</p>
                <p><strong>Delivery Fee:</strong> ₱{order['DeliveryFee']:.2f}</p>
                """
                self.details_label.setText(details_text)
        except Exception as e:
            self.details_label.setText(f"<p style='color: red;'>Error loading order details: {e}</p>")


class StatusUpdateDialog(QDialog):
    """Dialog to update order status"""

    def __init__(self, current_status, parent=None):
        super().__init__(parent)
        self.current_status = current_status
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Update Order Status")
        self.setMinimumWidth(400)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Title
        title = QLabel("Select New Status")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        layout.addWidget(title)

        # Current status
        current_label = QLabel(f"Current Status: {self.current_status}")
        current_label.setFont(QFont('Arial', 12))
        current_label.setStyleSheet("color: #666;")
        layout.addWidget(current_label)

        # Status combo box
        self.status_combo = QComboBox()
        self.status_combo.setMinimumHeight(45)
        self.status_combo.addItems([
            "Pending",
            "Preparing",
            "Out for Delivery",
            "Delivered",
            "Cancelled"
        ])
        self.status_combo.setCurrentText(self.current_status)
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.status_combo)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        update_btn = QPushButton("Update")
        update_btn.setMinimumHeight(45)
        update_btn.setMinimumWidth(120)
        update_btn.setStyleSheet("""
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
        """)
        update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        update_btn.clicked.connect(self.accept)
        button_layout.addWidget(update_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setMinimumWidth(120)
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
        """)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def get_selected_status(self):
        """Get the selected status"""
        return self.status_combo.currentText()