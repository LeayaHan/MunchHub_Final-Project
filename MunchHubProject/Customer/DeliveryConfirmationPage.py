"""
DeliveryConfirmationPage.py - Customer delivery confirmation page
Place this file in: Customer/DeliveryConfirmationPage.py
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from datetime import datetime


class DeliveryConfirmationPage(QWidget):
    """Page for customers to confirm delivery of orders"""

    def __init__(self, user_data, db_manager, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.db_manager = db_manager
        self.initUI()
        self.load_deliverable_orders()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("Confirm Delivery")
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #003274;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        refresh_btn.setFixedSize(120, 40)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
        refresh_btn.clicked.connect(self.load_deliverable_orders)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Info banner
        info_banner = QLabel(
            "✓ Orders marked as 'Out for delivery' will appear here\n"
            "✓ Click 'Confirm Delivery' when you receive your order\n"
            "✓ This helps us track successful deliveries"
        )
        info_banner.setFont(QFont('Arial', 10))
        info_banner.setStyleSheet("""
            color: #555;
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #2196F3;
            border-radius: 5px;
        """)
        info_banner.setWordWrap(True)
        layout.addWidget(info_banner)

        # Orders scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self.orders_container = QWidget()
        self.orders_layout = QVBoxLayout()
        self.orders_layout.setSpacing(15)
        self.orders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.orders_container.setLayout(self.orders_layout)

        scroll.setWidget(self.orders_container)
        layout.addWidget(scroll)

    def load_deliverable_orders(self):
        """Load orders that are out for delivery"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            query = """
                SELECT o.OrderID, o.TotalFee, o.DeliveryFee, o.Address,
                       o.OrderStatus, p.PaymentMethod,
                       (SELECT UpdateDate FROM OrderTrack 
                        WHERE OrderID = o.OrderID 
                        ORDER BY UpdateDate DESC LIMIT 1) as LastUpdate,
                       GROUP_CONCAT(CONCAT(m.ItemName, ' x', ol.Quantity) 
                                   SEPARATOR ', ') as Items
                FROM Orders o
                JOIN Payments p ON o.PaymentID = p.PaymentID
                JOIN OrderList ol ON o.OrderID = ol.OrderID
                JOIN MenuItems m ON ol.MenuID = m.MenuID
                WHERE o.CustomerID = %s 
                AND o.OrderStatus = 'Out for delivery'
                GROUP BY o.OrderID
                ORDER BY LastUpdate DESC
            """
            cursor.execute(query, (self.user_data['customer_id'],))
            orders = cursor.fetchall()
            cursor.close()

            self.display_orders(orders)

        except Exception as e:
            print(f"Error loading deliverable orders: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load orders: {str(e)}")

    def display_orders(self, orders):
        """Display orders in the layout"""
        # Clear existing widgets
        while self.orders_layout.count():
            child = self.orders_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not orders:
            empty_label = QLabel(
                "No orders waiting for delivery confirmation\n\n"
                "Orders marked as 'Out for delivery' will appear here"
            )
            empty_label.setFont(QFont('Arial', 14))
            empty_label.setStyleSheet("color: #999;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setMinimumHeight(200)
            self.orders_layout.addWidget(empty_label)
            return

        for order in orders:
            order_card = self.create_order_card(order)
            self.orders_layout.addWidget(order_card)

    def create_order_card(self, order):
        """Create a card widget for an order"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #FF9800;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        card.setLayout(layout)

        # Header row
        header_layout = QHBoxLayout()

        order_id_label = QLabel(f"Order #{order['OrderID']}")
        order_id_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        order_id_label.setStyleSheet("color: #003274;")
        header_layout.addWidget(order_id_label)

        status_label = QLabel("OUT FOR DELIVERY")
        status_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        status_label.setStyleSheet("""
            color: white;
            background-color: #FF9800;
            padding: 8px 15px;
            border-radius: 6px;
        """)
        header_layout.addWidget(status_label)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(separator)

        # Order details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(8)

        # Items
        items_label = QLabel(f"Items: {order['Items']}")
        items_label.setFont(QFont('Arial', 11))
        items_label.setStyleSheet("color: #333;")
        items_label.setWordWrap(True)
        details_layout.addWidget(items_label)

        # Address
        address_label = QLabel(f"Delivery to: {order['Address']}")
        address_label.setFont(QFont('Arial', 11))
        address_label.setStyleSheet("color: #333;")
        address_label.setWordWrap(True)
        details_layout.addWidget(address_label)

        # Payment
        payment_label = QLabel(f"Payment: {order['PaymentMethod']}")
        payment_label.setFont(QFont('Arial', 11))
        payment_label.setStyleSheet("color: #333;")
        details_layout.addWidget(payment_label)

        # Total
        total = order['TotalFee'] + order['DeliveryFee']
        total_label = QLabel(f"Total: ₱{total:.2f}")
        total_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        total_label.setStyleSheet("color: #4CAF50;")
        details_layout.addWidget(total_label)

        # Last update
        if order['LastUpdate']:
            last_update_str = order['LastUpdate'].strftime('%b %d, %Y at %I:%M %p')
            update_label = QLabel(f" Last update: {last_update_str}")
            update_label.setFont(QFont('Arial', 10))
            update_label.setStyleSheet("color: #666;")
            details_layout.addWidget(update_label)

        layout.addLayout(details_layout)

        # Action button
        confirm_btn = QPushButton("✓ Confirm Delivery Received")
        confirm_btn.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        confirm_btn.setMinimumHeight(50)
        confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm_btn.setStyleSheet("""
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
        confirm_btn.clicked.connect(lambda: self.confirm_delivery(order))
        layout.addWidget(confirm_btn)

        return card

    def confirm_delivery(self, order):
        """Confirm that delivery has been received"""
        reply = QMessageBox.question(
            self,
            'Confirm Delivery',
            f"Have you received Order #{order['OrderID']}?\n\n"
            "This will mark the order as delivered and complete.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.db_manager.connection.cursor(dictionary=True)

                # Update order status to Delivered
                cursor.execute(
                    "UPDATE Orders SET OrderStatus = 'Delivered' WHERE OrderID = %s",
                    (order['OrderID'],)
                )

                # Generate new TrackID
                cursor.execute("SELECT TrackID FROM OrderTrack ORDER BY TrackID DESC LIMIT 1")
                result = cursor.fetchone()
                if result:
                    last_num = int(result['TrackID'][1:])
                    new_track_id = f"T{str(last_num + 1).zfill(3)}"
                else:
                    new_track_id = "T001"

                # Add tracking record
                cursor.execute(
                    """INSERT INTO OrderTrack (TrackID, OrderID, Status, Notes, UpdateDate)
                       VALUES (%s, %s, 'Delivered', 'Confirmed by customer', %s)""",
                    (new_track_id, order['OrderID'], datetime.now())
                )

                self.db_manager.connection.commit()
                cursor.close()

                QMessageBox.information(
                    self,
                    'Success',
                    f"Order #{order['OrderID']} has been confirmed as delivered!\n\n"
                    "Thank you for your confirmation. 🎉"
                )

                # Reload orders
                self.load_deliverable_orders()

            except Exception as e:
                if self.db_manager.connection:
                    self.db_manager.connection.rollback()
                print(f"Error confirming delivery: {e}")
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Error", f"Failed to confirm delivery: {str(e)}")