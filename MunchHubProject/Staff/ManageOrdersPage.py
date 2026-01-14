"""
ManageOrdersPage.py - Manage Orders Page (View)
Place this file in: Staff/ManageOrdersPage.py
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Staff.OrderDialogs import OrderAcceptDialog


class ManageOrdersPage(QWidget):
    """Page for managing pending orders"""

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

        # Orders table
        self.orders_table = self.create_orders_table()
        layout.addWidget(self.orders_table)

    def create_header(self):
        """Create page header"""
        header_layout = QHBoxLayout()

        title = QLabel("Manage Pending Orders")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Accept button
        accept_btn = QPushButton("Accept Order")
        accept_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        accept_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        accept_btn.setFixedSize(150, 40)
        accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        accept_btn.clicked.connect(self.accept_selected_order)
        header_layout.addWidget(accept_btn)

        # Refresh button
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

    def create_orders_table(self):
        """Create orders table"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Order ID", "Customer", "Items", "Total", "Address", "Payment"
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
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
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
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(70)

        # Enable double-click to accept
        table.doubleClicked.connect(self.accept_selected_order)

        return table

    def load_data(self):
        """Load pending orders"""
        orders = self.controller.get_pending_orders()
        self.populate_table(orders)

    def populate_table(self, orders):
        """Populate table with orders"""
        self.orders_table.setRowCount(len(orders) if orders else 1)

        if not orders:
            empty_msg = QTableWidgetItem("No pending orders available")
            empty_msg.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_msg.setForeground(QColor('#999'))
            self.orders_table.setItem(0, 0, empty_msg)
            self.orders_table.setSpan(0, 0, 1, 6)
            return

        for row, order in enumerate(orders):
            # Store order data in the row
            self.orders_table.setRowHeight(row, 70)

            # Order ID
            id_item = QTableWidgetItem(order['OrderID'])
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            id_item.setForeground(QColor('#003274'))
            id_item.setData(Qt.ItemDataRole.UserRole, order)  # Store full order data
            self.orders_table.setItem(row, 0, id_item)

            # Customer
            customer_item = QTableWidgetItem(order['CustomerName'])
            customer_item.setForeground(QColor('black'))
            self.orders_table.setItem(row, 1, customer_item)

            # Items
            items_text = order['Items'][:50] + "..." if order['Items'] and len(order['Items']) > 50 else order['Items']
            items_item = QTableWidgetItem(items_text)
            items_item.setForeground(QColor('black'))
            items_item.setToolTip(order['Items'] or "")
            self.orders_table.setItem(row, 2, items_item)

            # Total
            total = float(order['TotalFee']) + float(order['DeliveryFee'])
            total_item = QTableWidgetItem(f"₱{total:.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            total_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            total_item.setForeground(QColor('#FF9800'))
            self.orders_table.setItem(row, 3, total_item)

            # Address
            address_text = order['Address'][:30] + "..." if len(order['Address']) > 30 else order['Address']
            address_item = QTableWidgetItem(address_text)
            address_item.setForeground(QColor('black'))
            address_item.setToolTip(order['Address'])
            self.orders_table.setItem(row, 4, address_item)

            # Payment
            payment_item = QTableWidgetItem(order['PaymentMethod'])
            payment_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            payment_item.setForeground(QColor('black'))
            self.orders_table.setItem(row, 5, payment_item)

    def apply_message_box_style(self):
        """Apply black text styling to message boxes"""
        QApplication.instance().setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 13px;
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

    def accept_selected_order(self):
        """Accept the selected order"""
        selected_row = self.orders_table.currentRow()

        if selected_row < 0:
            self.apply_message_box_style()
            QMessageBox.warning(
                self,
                'No Selection',
                'Please select an order from the table first!'
            )
            return

        # Get order data from the first column
        id_item = self.orders_table.item(selected_row, 0)
        if not id_item:
            return

        order = id_item.data(Qt.ItemDataRole.UserRole)
        if not order:
            self.apply_message_box_style()
            QMessageBox.warning(
                self,
                'Error',
                'Could not retrieve order data. Please refresh and try again.'
            )
            return

        # Open accept dialog
        dialog = OrderAcceptDialog(self, order, self.controller)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload data to refresh the table
            self.load_data()

            # Show success message with black text
            self.apply_message_box_style()
            QMessageBox.information(
                self,
                'Order Accepted',
                f'Order {order["OrderID"]} has been successfully accepted and is now being prepared!'
            )