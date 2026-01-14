"""
OrderDialogs.py - Dialog classes with TAX calculations displayed
FIXED: Constructor parameter mismatch
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class OrderVerificationDialog(QDialog):
    """Dialog to verify order before placing it - WITH TAX DISPLAY"""

    def __init__(self, parent, cart_items, subtotal, delivery_fee, user_data, tax_amount=0):  # FIXED: Added tax_amount parameter
        super().__init__(parent)
        self.cart_items = cart_items
        self.subtotal = subtotal
        self.delivery_fee = delivery_fee
        self.user_data = user_data
        self.tax_amount = tax_amount  # Store tax amount
        self.delivery_address = ''
        self.payment_method = 'Cash on delivery'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Verify Your Order - MunchHub')
        self.resize(650, 780)  # CHANGED: Increased height for tax line
        self.setMinimumSize(620, 780)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QLabel { background: transparent; border: none; color: black; }
            QScrollArea {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
            }
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                color: black;
                min-height: 28px;
                max-height: 28px;
            }
            QLineEdit:focus { border: 2px solid #ffbd59; }
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                color: black;
                min-height: 28px;
                max-height: 28px;
            }
            QComboBox:focus { border: 2px solid #ffbd59; }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 8px;
                min-height: 35px;
                max-height: 35px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # Header
        header = QLabel('Review Your Order')
        header.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #003274;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Order items scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        items_widget = QWidget()
        items_layout = QVBoxLayout(items_widget)
        items_layout.setSpacing(12)
        items_layout.setContentsMargins(12, 12, 12, 12)

        for item in self.cart_items:
            item_frame = self.create_item_frame(item)
            items_layout.addWidget(item_frame)

        scroll_area.setWidget(items_widget)
        layout.addWidget(scroll_area, 1)

        # Delivery address
        layout.addWidget(self.create_address_section())

        # Payment method
        layout.addWidget(self.create_payment_section())

        # Card number container
        self.card_container = self.create_card_section()
        layout.addWidget(self.card_container)

        # Cost summary WITH TAX
        layout.addWidget(self.create_summary_section())

        # Buttons
        layout.addLayout(self.create_buttons())

    def create_item_frame(self, item):
        """Create a single item frame"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #f9f9f9; border-radius: 8px; }")
        item_layout = QHBoxLayout(frame)
        item_layout.setContentsMargins(12, 10, 12, 10)

        details_layout = QVBoxLayout()
        name_label = QLabel(item['name'])
        name_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #003274;")

        qty_price = QLabel(f"Qty: {item['quantity']} × ₱{item['price']:.2f}")
        qty_price.setFont(QFont('Arial', 10))
        qty_price.setStyleSheet("color: #666;")

        details_layout.addWidget(name_label)
        details_layout.addWidget(qty_price)
        item_layout.addLayout(details_layout, 1)

        subtotal_label = QLabel(f"₱{item['subtotal']:.2f}")
        subtotal_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        subtotal_label.setStyleSheet("color: #ffbd59;")
        item_layout.addWidget(subtotal_label)

        return frame

    def create_address_section(self):
        """No default address, only placeholder"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #eef3f8;
                border: 2px solid #003274;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        address_label = QLabel("Delivery Address *")
        address_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        address_label.setStyleSheet("color: black;")
        layout.addWidget(address_label)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText(
            "Enter your complete delivery address (e.g., House #, Street, Barangay, City)")
        self.address_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 2px solid #003274;
                border-radius: 8px;
                padding: 8px;
                min-height: 28px;
                max-height: 28px;
            }
            QLineEdit:focus {
                border: 2px solid #ffbd59;
            }
        """)
        layout.addWidget(self.address_input)

        return container

    def create_payment_section(self):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #eef3f8;
                border: 2px solid #003274;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        label = QLabel("Payment Method *")
        label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        label.setStyleSheet("color: black;")
        layout.addWidget(label)

        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Cash on delivery", "Debit Card", "Credit Card"])
        self.payment_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 2px solid #003274;
                border-radius: 8px;
                padding: 8px;
                min-height: 28px;
                max-height: 28px;
            }
            QComboBox:focus {
                border: 2px solid #ffbd59;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #ffbd59;
                selection-color: black;
            }
        """)
        self.payment_combo.currentTextChanged.connect(self.toggle_card_input)
        layout.addWidget(self.payment_combo)

        return container

    def create_card_section(self):
        """Create card number section"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #eef3f8;
                border: 2px solid #003274;
                border-radius: 10px;
            }
        """)

        card_layout = QVBoxLayout(container)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(4)

        self.card_label = QLabel('Card Number * (8 digits)')
        self.card_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.card_label.setStyleSheet("color: black;")
        card_layout.addWidget(self.card_label)

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText('Enter 8-digit card number')
        self.card_input.setFont(QFont('Arial', 11))
        self.card_input.setMaxLength(8)
        self.card_input.setValidator(
            QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        )
        self.card_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 2px solid #003274;
                border-radius: 8px;
                padding: 8px;
                min-height: 28px;
                max-height: 28px;
            }
            QLineEdit:focus {
                border: 2px solid #ffbd59;
            }
        """)
        card_layout.addWidget(self.card_input)

        container.setVisible(False)
        container.setFixedHeight(0)
        return container

    def create_summary_section(self):
        """Create cost summary WITH TAX"""
        summary_frame = QFrame()
        summary_frame.setFixedHeight(190)  # Increased height for tax line
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #e0e0e0;
            }
        """)

        grid = QGridLayout(summary_frame)
        grid.setContentsMargins(12, 10, 12, 10)
        grid.setVerticalSpacing(6)

        def label(text, bold=False, color="black"):
            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold if bold else QFont.Weight.Normal))
            lbl.setStyleSheet(f"color: {color};")
            return lbl

        def value(text, bold=False, color="black"):
            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold if bold else QFont.Weight.Normal))
            lbl.setStyleSheet(f"color: {color};")
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            return lbl

        # Subtotal
        grid.addWidget(label("Subtotal:"), 0, 0)
        grid.addWidget(value(f"₱{self.subtotal:.2f}", True), 0, 1)

        # TAX - ADDED
        grid.addWidget(label("Tax (12% VAT):"), 1, 0)
        grid.addWidget(value(f"₱{self.tax_amount:.2f}", True, "#FF6B6B"), 1, 1)

        # Delivery Fee
        grid.addWidget(label("Delivery Fee:"), 2, 0)
        grid.addWidget(value(f"₱{self.delivery_fee:.2f}", True), 2, 1)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background:#ccc;")
        grid.addWidget(divider, 3, 0, 1, 2)

        # Total (with tax)
        grand_total = self.subtotal + self.tax_amount + self.delivery_fee
        grid.addWidget(label("Total:", True, "#003274"), 4, 0)
        grid.addWidget(value(f"₱{grand_total:.2f}", True, "#ff9800"), 4, 1)

        return summary_frame

    def create_buttons(self):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton { background-color: #e0e0e0; color: #333; }
            QPushButton:hover { background-color: #d0d0d0; }
        """)
        cancel_btn.clicked.connect(self.reject)

        confirm_btn = QPushButton('Place Order')
        confirm_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm_btn.setStyleSheet("""
            QPushButton { background-color: #003274; color: white; }
            QPushButton:hover { background-color: #004a9e; }
        """)
        confirm_btn.clicked.connect(self.confirm_order)

        button_layout.addWidget(cancel_btn, 1)
        button_layout.addWidget(confirm_btn, 1)
        return button_layout

    def toggle_card_input(self, payment_method):
        """Show/hide card input based on payment method"""
        show_card = payment_method in ['Debit Card', 'Credit Card']

        if show_card:
            self.card_container.setVisible(True)
            self.card_container.setFixedHeight(70)
        else:
            self.card_container.setVisible(False)
            self.card_container.setFixedHeight(0)
            self.card_input.clear()

    def confirm_order(self):
        """Validate and confirm order"""
        self.delivery_address = self.address_input.text().strip()
        self.payment_method = self.payment_combo.currentText()

        if not self.delivery_address:
            QMessageBox.warning(
                self,
                'Missing Address',
                'Please enter your delivery address!\n\n'
                'This field is required and cannot be empty.'
            )
            self.address_input.setFocus()
            return

        if len(self.delivery_address) < 10:
            QMessageBox.warning(
                self,
                'Incomplete Address',
                'Please enter a complete delivery address!\n\n'
                'Your address should include:\n'
                '• House/Building number\n'
                '• Street name\n'
                '• Barangay/District\n'
                '• City/Municipality'
            )
            self.address_input.setFocus()
            return

        # Card validation
        if self.payment_method in ['Debit Card', 'Credit Card']:
            card_number = self.card_input.text().strip()
            if len(card_number) != 8 or not card_number.isdigit():
                QMessageBox.warning(
                    self,
                    'Invalid Card Number',
                    'Card number must be exactly 8 digits!'
                )
                self.card_input.setFocus()
                return
            self.card_number = f"****{card_number[-4:]}"
        else:
            self.card_number = None

        self.accept()

    def get_order_details(self):
        """Return order details"""
        details = {
            'address': self.delivery_address,
            'payment_method': self.payment_method
        }
        if hasattr(self, 'card_number') and self.card_number:
            details['card_number'] = self.card_number
        return details


class OrderHistoryDialog(QDialog):
    """Dialog to display order history"""

    def __init__(self, parent, customer_id, db_manager):
        super().__init__(parent)
        self.customer_id = customer_id
        self.db_manager = db_manager
        self.initUI()
        self.load_orders()

    def initUI(self):
        self.setWindowTitle('Order History - MunchHub')
        self.setMinimumSize(900, 600)
        self.setModal(True)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header with refresh button
        header_layout = self.create_header()
        layout.addLayout(header_layout)

        # Orders table
        self.orders_table = self.create_orders_table()
        layout.addWidget(self.orders_table)

        # Close button
        close_btn = self.create_close_button()
        layout.addWidget(close_btn)

    def create_header(self):
        """Create header with title and refresh button"""
        header_layout = QHBoxLayout()

        header = QLabel('Order History')
        header.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        header.setStyleSheet("color: #003274;")
        header_layout.addWidget(header)
        header_layout.addStretch()

        refresh_btn = QPushButton('Refresh')
        refresh_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        refresh_btn.setFixedHeight(35)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        refresh_btn.clicked.connect(self.load_orders)
        header_layout.addWidget(refresh_btn)

        return header_layout

    def create_orders_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Order ID", "Date", "Total", "Payment", "Status", "Action"
        ])

        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                gridline-color: #ccc;
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
                font-size: 11px;
            }
            QTableWidget {
                alternate-background-color: #f7f9fc;
            }
        """)

        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(60)

        return table

    def create_close_button(self):
        """Create close button"""
        close_btn = QPushButton('Close')
        close_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        close_btn.setMinimumHeight(45)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #616161; }
        """)
        close_btn.clicked.connect(self.accept)
        return close_btn

    def load_orders(self):
        """Load orders from database"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            query = """
                SELECT o.OrderID, o.TotalFee, o.Tax, o.DeliveryFee, o.OrderStatus, 
                       o.Address, p.PaymentMethod,
                       (SELECT MIN(ot.UpdateDate) 
                        FROM OrderTrack ot 
                        WHERE ot.OrderID = o.OrderID) as OrderDate
                FROM Orders o
                JOIN Payments p ON o.PaymentID = p.PaymentID
                WHERE o.CustomerID = %s
                ORDER BY o.OrderID DESC
            """
            cursor.execute(query, (self.customer_id,))
            orders = cursor.fetchall()
            cursor.close()

            self.populate_table(orders)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load order history: {str(e)}')

    def populate_table(self, orders):
        """Populate table with order data"""
        self.orders_table.setRowCount(len(orders) if orders else 1)

        if not orders:
            empty_msg = QTableWidgetItem("No orders found")
            empty_msg.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_msg.setForeground(QColor('black'))
            empty_msg.setFlags(empty_msg.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.orders_table.setItem(0, 0, empty_msg)
            self.orders_table.setSpan(0, 0, 1, 6)
            return

        status_colors = {
            'Pending': '#FF9800',
            'Preparing': '#2196F3',
            'Out for delivery': '#9C27B0',
            'Delivered': '#4CAF50',
            'Cancelled': '#F44336'
        }

        for row, order in enumerate(orders):
            # Order ID
            order_id_item = QTableWidgetItem(order['OrderID'])
            order_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            order_id_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            order_id_item.setForeground(QColor('black'))
            order_id_item.setFlags(order_id_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.orders_table.setItem(row, 0, order_id_item)

            # Date
            order_date = order.get('OrderDate')
            date_str = order_date.strftime('%b %d, %Y') if order_date else 'N/A'
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setForeground(QColor('black'))
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.orders_table.setItem(row, 1, date_item)

            # Total (TotalFee already includes tax from database)
            total = float(order['TotalFee'])
            total_item = QTableWidgetItem(f"₱{total:.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            total_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            total_item.setForeground(QColor('black'))
            total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.orders_table.setItem(row, 2, total_item)

            # Payment Method
            payment_item = QTableWidgetItem(order['PaymentMethod'])
            payment_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            payment_item.setForeground(QColor('black'))
            payment_item.setFlags(payment_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.orders_table.setItem(row, 3, payment_item)

            # Status
            status_item = QTableWidgetItem(order['OrderStatus'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            status_item.setForeground(QColor(status_colors.get(order['OrderStatus'], '#666')))
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.orders_table.setItem(row, 4, status_item)

            # Action button
            action_widget = self.create_action_button(order)
            self.orders_table.setCellWidget(row, 5, action_widget)

    def create_action_button(self, order):
        """Create action button widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if order["OrderStatus"] == "Pending":
            cancel_btn = QPushButton("Cancel Order")
            cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            cancel_btn.setFixedSize(130, 38)
            cancel_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    font-weight: bold;
                    border-radius: 6px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                }
            """)
            cancel_btn.clicked.connect(lambda: self.cancel_order(order))
            layout.addWidget(cancel_btn, 0, Qt.AlignmentFlag.AlignCenter)
        else:
            no_action_label = QLabel("—")
            no_action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_action_label.setStyleSheet("color: #999; font-size: 14px;")
            layout.addWidget(no_action_label, 0, Qt.AlignmentFlag.AlignCenter)

        return widget

    def cancel_order(self, order):
        """Cancel an order"""
        QApplication.instance().setStyleSheet("""
            QMessageBox QLabel { color: black; }
            QMessageBox QPushButton { color: black; }
        """)

        confirm = QMessageBox.question(
            self,
            "Cancel Order",
            f"Are you sure you want to cancel Order {order['OrderID']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.db_manager.connection.cursor()
                cursor.execute(
                    "UPDATE Orders SET OrderStatus='Cancelled' WHERE OrderID=%s",
                    (order["OrderID"],)
                )
                self.db_manager.connection.commit()
                cursor.close()
                QMessageBox.information(self, "Success", f"Order {order['OrderID']} has been cancelled.")
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel order: {str(e)}")


class EnhancedOrderHistoryDialog(QDialog):
    """
    Enhanced Order History Dialog with detailed tracking timeline
    Replace the old OrderHistoryDialog with this version
    """

    def __init__(self, parent, customer_id, db_manager):
        super().__init__(parent)
        self.customer_id = customer_id
        self.db_manager = db_manager
        self.selected_order_id = None
        self.initUI()
        self.load_orders()

    def initUI(self):
        self.setWindowTitle('Order History - MunchHub')
        self.setMinimumSize(1100, 650)
        self.setModal(True)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Left side - Orders list
        left_panel = self.create_orders_panel()
        main_layout.addWidget(left_panel, 3)

        # Right side - Order tracking timeline
        right_panel = self.create_tracking_panel()
        main_layout.addWidget(right_panel, 2)

    def create_orders_panel(self):
        """Create left panel with orders list"""
        panel = QWidget()
        panel.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        header = QLabel('📋 Your Orders')
        header.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #003274;")
        header_layout.addWidget(header)
        header_layout.addStretch()

        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        refresh_btn.setFixedHeight(35)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        refresh_btn.clicked.connect(self.load_orders)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Orders table
        self.orders_table = self.create_orders_table()
        layout.addWidget(self.orders_table)

        # Close button
        close_btn = QPushButton('Close')
        close_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        close_btn.setMinimumHeight(45)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #616161; }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        return panel

    def create_tracking_panel(self):
        """Create right panel with order tracking timeline"""
        panel = QWidget()
        panel.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel('📍 Order Tracking')
        header.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        header.setStyleSheet("color: #003274;")
        layout.addWidget(header)

        # Timeline container
        self.timeline_scroll = QScrollArea()
        self.timeline_scroll.setWidgetResizable(True)
        self.timeline_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.timeline_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self.timeline_container = QWidget()
        self.timeline_layout = QVBoxLayout(self.timeline_container)
        self.timeline_layout.setSpacing(10)
        self.timeline_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initial message
        initial_msg = QLabel('← Select an order to view tracking details')
        initial_msg.setStyleSheet("color: #999; font-size: 13px; padding: 20px;")
        initial_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        initial_msg.setWordWrap(True)
        self.timeline_layout.addWidget(initial_msg)

        self.timeline_scroll.setWidget(self.timeline_container)
        layout.addWidget(self.timeline_scroll, 1)

        return panel

    def create_orders_table(self):
        """Create orders table"""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Order ID", "Date", "Total", "Payment", "Status"
        ])

        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                color: black;
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #003274;
            }
            QHeaderView::section {
                background-color: #003274;
                color: white;
                padding: 12px;
                font-weight: bold;
                font-size: 11px;
                border: none;
            }
        """)

        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(50)

        # Connect selection signal
        table.itemSelectionChanged.connect(self.on_order_selected)

        return table

    def load_orders(self):
        """Load orders from database"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            query = """
                SELECT o.OrderID, o.TotalFee, o.DeliveryFee, o.OrderStatus, 
                       o.Address, p.PaymentMethod, o.OrderDate
                FROM Orders o
                JOIN Payments p ON o.PaymentID = p.PaymentID
                WHERE o.CustomerID = %s
                ORDER BY o.OrderDate DESC
            """
            cursor.execute(query, (self.customer_id,))
            orders = cursor.fetchall()
            cursor.close()

            self.populate_table(orders)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load order history: {str(e)}')

    def populate_table(self, orders):
        """Populate table with order data"""
        self.orders_table.setRowCount(len(orders) if orders else 1)

        if not orders:
            empty_msg = QTableWidgetItem("No orders found")
            empty_msg.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_msg.setForeground(QColor('black'))
            self.orders_table.setItem(0, 0, empty_msg)
            self.orders_table.setSpan(0, 0, 1, 5)
            return

        status_colors = {
            'Pending': '#FF9800',
            'Preparing': '#2196F3',
            'Out for delivery': '#9C27B0',
            'Delivered': '#4CAF50',
            'Cancelled': '#F44336'
        }

        for row, order in enumerate(orders):
            # Order ID
            order_id_item = QTableWidgetItem(order['OrderID'])
            order_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            order_id_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            order_id_item.setForeground(QColor('#003274'))
            order_id_item.setData(Qt.ItemDataRole.UserRole, order)  # Store full order data
            self.orders_table.setItem(row, 0, order_id_item)

            # Date
            order_date = order.get('OrderDate')
            date_str = order_date.strftime('%b %d, %I:%M %p') if order_date else 'N/A'
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setFont(QFont('Arial', 9))
            date_item.setForeground(QColor('black'))
            self.orders_table.setItem(row, 1, date_item)

            # Total
            total = float(order['TotalFee']) + float(order['DeliveryFee'])
            total_item = QTableWidgetItem(f"₱{total:.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            total_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            total_item.setForeground(QColor('black'))
            self.orders_table.setItem(row, 2, total_item)

            # Payment
            payment_item = QTableWidgetItem(order['PaymentMethod'])
            payment_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            payment_item.setFont(QFont('Arial', 9))
            payment_item.setForeground(QColor('black'))
            self.orders_table.setItem(row, 3, payment_item)

            # Status
            status_item = QTableWidgetItem(order['OrderStatus'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            status_item.setForeground(QColor(status_colors.get(order['OrderStatus'], '#666')))
            self.orders_table.setItem(row, 4, status_item)

    def on_order_selected(self):
        """Handle order selection - load tracking timeline"""
        selected_items = self.orders_table.selectedItems()
        if not selected_items:
            return

        # Get order data from first column
        order_data = self.orders_table.item(selected_items[0].row(), 0).data(Qt.ItemDataRole.UserRole)
        if not order_data:
            return

        self.selected_order_id = order_data['OrderID']
        self.load_order_tracking(order_data)

    def load_order_tracking(self, order_data):
        """Load tracking timeline for selected order"""
        try:
            # Clear timeline
            while self.timeline_layout.count():
                child = self.timeline_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Add order info header
            info_frame = QFrame()
            info_frame.setStyleSheet("""
                QFrame {
                    background-color: #E3F2FD;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            info_layout = QVBoxLayout(info_frame)

            order_id_label = QLabel(f"📦 Order {order_data['OrderID']}")
            order_id_label.setFont(QFont('Arial', 13, QFont.Weight.Bold))
            order_id_label.setStyleSheet("color: #003274;")
            info_layout.addWidget(order_id_label)

            address_label = QLabel(f"📍 {order_data['Address']}")
            address_label.setFont(QFont('Arial', 10))
            address_label.setStyleSheet("color: #666;")
            address_label.setWordWrap(True)
            info_layout.addWidget(address_label)

            self.timeline_layout.addWidget(info_frame)

            # Get tracking records
            cursor = self.db_manager.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT Status, Notes, UpdateDate
                FROM OrderTrack
                WHERE OrderID = %s
                ORDER BY UpdateDate DESC
            """, (order_data['OrderID'],))

            tracking_records = cursor.fetchall()
            cursor.close()

            if not tracking_records:
                no_tracking = QLabel('No tracking information available yet')
                no_tracking.setStyleSheet("color: #999; padding: 20px;")
                no_tracking.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.timeline_layout.addWidget(no_tracking)
                return

            # Add timeline items
            for i, record in enumerate(tracking_records):
                is_latest = (i == 0)
                timeline_item = self.create_timeline_item(record, is_latest)
                self.timeline_layout.addWidget(timeline_item)

        except Exception as e:
            error_label = QLabel(f'Error loading tracking: {str(e)}')
            error_label.setStyleSheet("color: #F44336; padding: 10px;")
            error_label.setWordWrap(True)
            self.timeline_layout.addWidget(error_label)

    def create_timeline_item(self, record, is_latest):
        """Create a timeline item widget"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {'#FFF3E0' if is_latest else '#f9f9f9'};
                border-left: 4px solid {'#FF9800' if is_latest else '#e0e0e0'};
                border-radius: 6px;
                padding: 10px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        # Status with icon
        status_icons = {
            'Confirmed': '✅',
            'Preparing': '👨‍🍳',
            'Ready': '📦',
            'Out for Delivery': '🚚',
            'Delivered': '🎉',
            'Cancelled': '❌'
        }

        status_label = QLabel(f"{status_icons.get(record['Status'], '•')} {record['Status']}")
        status_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        status_label.setStyleSheet("color: #003274;")
        layout.addWidget(status_label)

        # Notes
        if record.get('Notes'):
            notes_label = QLabel(record['Notes'])
            notes_label.setFont(QFont('Arial', 9))
            notes_label.setStyleSheet("color: #666;")
            notes_label.setWordWrap(True)
            layout.addWidget(notes_label)

        # Time
        time_str = record['UpdateDate'].strftime('%b %d, %I:%M %p') if record.get('UpdateDate') else 'N/A'
        time_label = QLabel(f"🕐 {time_str}")
        time_label.setFont(QFont('Arial', 9))
        time_label.setStyleSheet("color: #999;")
        layout.addWidget(time_label)

        return frame
