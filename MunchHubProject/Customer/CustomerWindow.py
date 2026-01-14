"""
CustomerWindow.py - Main customer window with tax calculations
MODIFICATIONS:
1. Added TAX_RATE constant (12% VAT)
2. Updated all price displays to include tax
3. Modified checkout flow to show tax breakdown
4. Updated database to store tax amounts
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# Import MVC components
try:
    from Customer.MenuModel import MenuModel
    from Customer.CartModel import CartModel
    from Customer.CustomerController import CustomerController
    from Customer.OrderDialogs import OrderVerificationDialog, OrderHistoryDialog
    from Customer.MenuWidgets import MenuItemWidget, CartItemWidget
    from Customer.DeliveryConfirmationPage import DeliveryConfirmationPage
except ImportError:
    try:
        from MenuModel import MenuModel
        from CartModel import CartModel
        from CustomerController import CustomerController
        from OrderDialogs import OrderVerificationDialog, OrderHistoryDialog
        from MenuWidgets import MenuItemWidget, CartItemWidget
        from DeliveryConfirmationPage import DeliveryConfirmationPage
    except ImportError as e:
        print(f"Error: Could not import components - {e}")


class CustomerWindow(QMainWindow):
    """Main customer window with tax calculations"""

    # Tax rate constant (12% VAT)
    TAX_RATE = 0.12

    def __init__(self, user_data, db_manager):
        super().__init__()
        self.user_data = user_data
        self.db_manager = db_manager

        # Initialize MVC components
        self.menu_model = MenuModel(db_manager)
        self.cart_model = CartModel()
        self.controller = CustomerController(
            self.menu_model,
            self.cart_model,
            db_manager,
            user_data
        )

        # Current selected category
        self.selected_category = 'all'
        self.current_page = 'menu'

        self.initUI()
        self.load_initial_data()

    def calculate_tax(self, amount):
        """Calculate tax for given amount"""
        return amount * self.TAX_RATE

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle('MunchHub - Customer Dashboard')
        self.setMinimumSize(1200, 750)
        self.setStyleSheet("background-color: #ffffff;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Top Header
        main_layout.addWidget(self.create_header())

        # Content Area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: white;")

        # Page 1: Menu and Cart
        self.menu_page = self.create_menu_page()
        self.content_stack.addWidget(self.menu_page)

        # Page 2: Delivery Confirmation
        self.delivery_page = DeliveryConfirmationPage(self.user_data, self.db_manager)
        self.delivery_page.setStyleSheet("background-color: #f5f5f5;")
        self.content_stack.addWidget(self.delivery_page)

        main_layout.addWidget(self.content_stack, 1)

    def create_header(self):
        """Create header bar with logo and buttons"""
        header_bar = QWidget()
        header_bar.setStyleSheet("background-color: #002052; padding: 15px;")
        header_bar.setFixedHeight(80)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(30, 0, 30, 0)
        header_bar.setLayout(header_layout)

        # Logo/Title
        title_label = QLabel('MunchHub')
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffbd59;")
        header_layout.addWidget(title_label)

        # Welcome message
        welcome_label = QLabel(f'Welcome, {self.user_data["full_name"]}!')
        welcome_label.setFont(QFont('Arial', 14))
        welcome_label.setStyleSheet("color: white;")
        header_layout.addStretch()
        header_layout.addWidget(welcome_label)

        header_layout.addSpacing(15)

        # Menu button
        self.menu_btn = QPushButton('Menu')
        self.menu_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        self.menu_btn.setMinimumSize(120, 45)
        self.menu_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd59;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover { 
                background-color: #ffc970;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #e6a84d;
                color: #000000;
            }
        """)
        self.menu_btn.clicked.connect(self.show_menu_page)
        header_layout.addWidget(self.menu_btn)
        header_layout.addSpacing(10)

        # Delivery Confirmation button
        self.delivery_btn = QPushButton('Deliveries')
        self.delivery_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        self.delivery_btn.setMinimumSize(120, 45)
        self.delivery_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.delivery_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delivery_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd59;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover { 
                background-color: #ffc970;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #e6a84d;
                color: #000000;
            }
        """)
        self.delivery_btn.clicked.connect(self.show_delivery_page)
        header_layout.addWidget(self.delivery_btn)
        header_layout.addSpacing(10)

        # Order History button
        history_btn = QPushButton('History')
        history_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        history_btn.setMinimumSize(120, 45)
        history_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        history_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd59;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover { 
                background-color: #ffc970;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #e6a84d;
                color: #000000;
            }
        """)
        history_btn.clicked.connect(self.show_order_history)
        header_layout.addWidget(history_btn)
        header_layout.addSpacing(10)

        # Logout button
        logout_btn = QPushButton('Logout')
        logout_btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        logout_btn.setMinimumSize(120, 45)
        logout_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd59;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover { 
                background-color: #ffc970;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #e6a84d;
                color: #000000;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)

        return header_bar

    def create_menu_page(self):
        """Create the menu and cart page"""
        page = QWidget()
        page.setStyleSheet("background-color: white;")
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        page.setLayout(content_layout)

        # Left Panel - Menu
        content_layout.addWidget(self.create_menu_panel(), 2)

        # Right Panel - Cart
        content_layout.addWidget(self.create_cart_panel())

        return page

    def show_menu_page(self):
        """Switch to menu page"""
        self.current_page = 'menu'
        self.content_stack.setCurrentIndex(0)
        self.highlight_active_button(self.menu_btn)

    def show_delivery_page(self):
        """Switch to delivery confirmation page"""
        self.current_page = 'delivery'
        self.content_stack.setCurrentIndex(1)
        self.delivery_page.load_deliverable_orders()
        self.highlight_active_button(self.delivery_btn)

    def highlight_active_button(self, active_btn):
        """Highlight the active navigation button"""
        default_style = """
            QPushButton {
                background-color: #ffbd59;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover { 
                background-color: #ffc970;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #e6a84d;
                color: #000000;
            }
        """

        active_style = """
            QPushButton {
                background-color: #e6a84d;
                color: #000000;
                border: 3px solid #002052;
                border-radius: 8px;
                padding: 5px 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6a84d;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #d69940;
                color: #000000;
            }
        """

        self.menu_btn.setStyleSheet(default_style)
        self.delivery_btn.setStyleSheet(default_style)

        if active_btn == self.menu_btn:
            self.menu_btn.setStyleSheet(active_style)
        elif active_btn == self.delivery_btn:
            self.delivery_btn.setStyleSheet(active_style)

    def create_menu_panel(self):
        """Create left menu panel with categories and items"""
        panel = QWidget()
        panel.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        panel.setLayout(layout)

        # Title and search bar
        top_section = QHBoxLayout()

        menu_title = QLabel('Our Menu')
        menu_title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        menu_title.setStyleSheet("color: #003274;")
        top_section.addWidget(menu_title)

        top_section.addStretch()

        # Category dropdown
        category_label = QLabel('Category:')
        category_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        category_label.setStyleSheet("color: #003274;")
        top_section.addWidget(category_label)

        self.category_dropdown = QComboBox()
        self.category_dropdown.setFixedWidth(220)
        self.category_dropdown.setMinimumHeight(45)
        self.category_dropdown.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.category_dropdown.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #ffbd59;
                border-radius: 8px;
                background-color: white;
                color: #003274;
                font-weight: bold;
            }
            QComboBox:hover {
                background-color: #fff5e6;
                border: 2px solid #ffa726;
            }
            QComboBox::drop-down {
                border: none;
                width: 35px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #003274;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #ffbd59;
                selection-background-color: #ffbd59;
                selection-color: #003274;
                padding: 5px;
                font-size: 11px;
            }
        """)
        self.category_dropdown.currentIndexChanged.connect(self.on_dropdown_changed)
        top_section.addWidget(self.category_dropdown)

        # Search box
        search_label = QLabel('Search:')
        search_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        search_label.setStyleSheet("color: #003274; margin-left: 20px;")
        top_section.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search menu items...')
        self.search_input.setFixedWidth(200)
        self.search_input.setMinimumHeight(45)
        self.search_input.setFont(QFont('Arial', 11))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                color: #333;
            }
            QLineEdit:hover {
                border: 2px solid #ffbd59;
            }
            QLineEdit:focus { 
                border: 2px solid #ffbd59;
                background-color: #fffef8;
            }
        """)
        self.search_input.textChanged.connect(self.on_search_changed)
        top_section.addWidget(self.search_input)

        layout.addLayout(top_section)

        # Menu items scroll area
        menu_scroll = QScrollArea()
        menu_scroll.setWidgetResizable(True)
        menu_scroll.setFrameShape(QFrame.Shape.NoFrame)
        menu_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #003274;
                border-radius: 6px;
            }
        """)

        self.menu_container = QWidget()
        self.menu_container.setStyleSheet("background-color: transparent;")
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setSpacing(15)
        self.menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.menu_container.setLayout(self.menu_layout)
        menu_scroll.setWidget(self.menu_container)

        layout.addWidget(menu_scroll, 1)
        return panel

    def create_cart_panel(self):
        """Create right cart panel with tax display and white cart items"""
        panel = QWidget()
        panel.setFixedWidth(380)
        panel.setStyleSheet("QWidget { background-color: #003274; border-radius: 15px; }")
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        panel.setLayout(layout)

        # Cart title
        cart_title = QLabel('Your Cart')
        cart_title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        cart_title.setStyleSheet("color: white; background-color: transparent;")
        layout.addWidget(cart_title)

        # Cart items scroll area
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)
        cart_scroll.setFrameShape(QFrame.Shape.NoFrame)
        cart_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #003274;
                border-radius: 5px;
            }
        """)

        self.cart_container = QWidget()
        self.cart_container.setStyleSheet("background-color: transparent;")
        self.cart_layout = QVBoxLayout()
        self.cart_layout.setSpacing(10)
        self.cart_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cart_container.setLayout(self.cart_layout)

        empty_label = QLabel('Your cart is empty')
        empty_label.setStyleSheet("color: white; font-size: 14px; background-color: transparent;")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cart_layout.addWidget(empty_label)

        cart_scroll.setWidget(self.cart_container)
        layout.addWidget(cart_scroll, 1)

        # Summary with tax breakdown
        summary_container = QWidget()
        summary_container.setStyleSheet(
            "background-color: #f9f9f9; border-radius: 8px; padding: 10px;"
        )
        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(5)
        summary_container.setLayout(summary_layout)

        self.subtotal_label = QLabel('Subtotal: ₱0.00')
        self.subtotal_label.setFont(QFont('Arial', 13))
        self.subtotal_label.setStyleSheet("color: #003274; background-color: transparent;")
        self.subtotal_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        summary_layout.addWidget(self.subtotal_label)

        self.tax_label = QLabel('Tax (12%): ₱0.00')
        self.tax_label.setFont(QFont('Arial', 13))
        self.tax_label.setStyleSheet("color: #003274; background-color: transparent;")
        self.tax_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        summary_layout.addWidget(self.tax_label)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #003274; max-height: 2px;")
        summary_layout.addWidget(separator)

        self.total_label = QLabel('Total: ₱0.00')
        self.total_label.setFont(QFont('Arial', 15, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #003274; background-color: transparent;")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        summary_layout.addWidget(self.total_label)

        layout.addWidget(summary_container)

        # Checkout button
        self.checkout_btn = QPushButton('Checkout')
        self.checkout_btn.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.checkout_btn.setMinimumHeight(55)
        self.checkout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkout_btn.setEnabled(False)
        self.checkout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #003274;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover:enabled {
                background-color: #ffbd59;
                color: #003274;
            }
            QPushButton:disabled {
                background-color: white;
                color: #003274;
                opacity: 0.6;
            }
        """)
        self.checkout_btn.clicked.connect(self.proceed_to_checkout)
        layout.addWidget(self.checkout_btn)

        return panel

    def load_initial_data(self):
        """Load categories and menu items"""
        success, message = self.controller.initialize_data()
        if not success:
            QApplication.instance().setStyleSheet("QMessageBox QLabel { color: black; }")
            QMessageBox.critical(self, 'Error', message)
            return

        self.display_categories()
        self.display_menu_items()
        self.highlight_active_button(self.menu_btn)

    def display_categories(self):
        """Populate category dropdown"""
        self.category_dropdown.blockSignals(True)
        self.category_dropdown.clear()
        self.category_dropdown.addItem('All Items', 'all')

        for category in self.menu_model.categories:
            count = self.menu_model.get_category_count(category['CategoryID'])
            dropdown_text = f"{category['CategoryName']} ({count})"
            self.category_dropdown.addItem(dropdown_text, category['CategoryID'])

        self.category_dropdown.blockSignals(False)

    def on_category_clicked(self, category_id):
        """Handle category selection"""
        self.selected_category = category_id
        self.search_input.clear()

        self.category_dropdown.blockSignals(True)
        for i in range(self.category_dropdown.count()):
            if self.category_dropdown.itemData(i) == category_id:
                self.category_dropdown.setCurrentIndex(i)
                break
        self.category_dropdown.blockSignals(False)

        filtered_items = self.controller.filter_menu_by_category(category_id)
        self.display_menu_items(filtered_items)

    def on_dropdown_changed(self, index):
        """Handle dropdown selection change"""
        if index >= 0:
            category_id = self.category_dropdown.itemData(index)
            self.on_category_clicked(category_id)

    def on_search_changed(self):
        """Handle search text change"""
        search_text = self.search_input.text().strip()
        results = self.controller.search_menu(search_text)
        self.display_menu_items(results)

    def display_menu_items(self, items=None):
        """Display menu items"""
        while self.menu_layout.count():
            child = self.menu_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if items is None:
            items = self.menu_model.filtered_items

        if not items:
            if self.search_input.text().strip():
                message = f'No items found for "{self.search_input.text()}"\n\nTry a different search term'
            else:
                category_name = 'this category'
                for i in range(self.category_dropdown.count()):
                    if self.category_dropdown.itemData(i) == self.selected_category:
                        category_name = self.category_dropdown.itemText(i)
                        break
                message = f'No items available in {category_name}\n\nTry selecting a different category'

            no_items_label = QLabel(message)
            no_items_label.setStyleSheet("color: #003274; font-size: 16px;")
            no_items_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.menu_layout.addWidget(no_items_label)
            return

        if self.selected_category != 'all' and not self.search_input.text().strip():
            category_name = ''
            for i in range(self.category_dropdown.count()):
                if self.category_dropdown.itemData(i) == self.selected_category:
                    category_name = self.category_dropdown.itemText(i).split(' (')[0]
                    break

            if category_name:
                header_frame = QFrame()
                header_frame.setStyleSheet("""
                    QFrame {
                        background-color: #ffbd59;
                        border-radius: 8px;
                        padding: 10px;
                    }
                """)
                header_layout = QHBoxLayout(header_frame)

                category_header = QLabel(f'{category_name}')
                category_header.setFont(QFont('Arial', 14, QFont.Weight.Bold))
                category_header.setStyleSheet("color: #003274;")

                item_count = QLabel(f'{len(items)} item{"s" if len(items) != 1 else ""}')
                item_count.setFont(QFont('Arial', 12))
                item_count.setStyleSheet("color: #003274;")

                header_layout.addWidget(category_header)
                header_layout.addStretch()
                header_layout.addWidget(item_count)

                self.menu_layout.addWidget(header_frame)

        for item in items:
            item_widget = MenuItemWidget(item)
            item_widget.item_added.connect(self.on_item_added_to_cart)
            self.menu_layout.addWidget(item_widget)

    def on_item_added_to_cart(self, item):
        """Handle item added to cart"""
        self.controller.add_to_cart(item)
        self.update_cart_display()

    def update_cart_display(self):
        """Update cart display with tax calculations"""
        while self.cart_layout.count():
            child = self.cart_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        cart_summary = self.controller.get_cart_summary()

        if cart_summary['is_empty']:
            empty_label = QLabel('Your cart is empty')
            empty_label.setStyleSheet("color: #999; font-size: 14px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_layout.addWidget(empty_label)

            self.subtotal_label.setText('Subtotal: ₱0.00')
            self.tax_label.setText('Tax (12%): ₱0.00')
            self.total_label.setText('Total: ₱0.00')
            self.checkout_btn.setEnabled(False)
            return

        for cart_item in cart_summary['items']:
            cart_widget = CartItemWidget(cart_item)
            cart_widget.quantity_changed.connect(self.on_cart_quantity_changed)
            cart_widget.item_removed.connect(self.on_cart_item_removed)
            self.cart_layout.addWidget(cart_widget)

        # Calculate tax
        subtotal = cart_summary['subtotal']
        tax = self.calculate_tax(subtotal)
        total = subtotal + tax

        self.subtotal_label.setText(f'Subtotal: ₱{subtotal:.2f}')
        self.tax_label.setText(f'Tax (12%): ₱{tax:.2f}')
        self.total_label.setText(f'Total: ₱{total:.2f}')
        self.checkout_btn.setEnabled(True)

    def on_cart_quantity_changed(self, cart_item, change):
        """Handle cart quantity change"""
        current_quantity = cart_item['quantity']

        if change < 0 and current_quantity + change <= 0:
            QApplication.instance().setStyleSheet("""
                QMessageBox QLabel { color: black; }
                QMessageBox QPushButton { 
                    color: black; 
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    padding: 5px 15px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)

            reply = QMessageBox.question(
                self,
                'Remove Item',
                f'Remove "{cart_item["name"]}" from your cart?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.controller.remove_from_cart(cart_item)
                self.update_cart_display()
        else:
            self.controller.update_cart_quantity(cart_item, change)
            self.update_cart_display()

    def on_cart_item_removed(self, cart_item):
        """Handle cart item removal"""
        QApplication.instance().setStyleSheet("""
            QMessageBox QLabel { color: black; }
            QMessageBox QPushButton { 
                color: black; 
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        reply = QMessageBox.question(
            self,
            'Remove Item',
            f'Are you sure you want to remove "{cart_item["name"]}" from your cart?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.remove_from_cart(cart_item)
            self.update_cart_display()

    def proceed_to_checkout(self):
        """Proceed to checkout with tax calculations"""
        cart_summary = self.controller.get_cart_summary()
        if cart_summary['is_empty']:
            return

        # Calculate tax for verification dialog
        subtotal = cart_summary['subtotal']
        tax = self.calculate_tax(subtotal)

        # Pass tax to verification dialog
        dialog = OrderVerificationDialog(
            self,
            cart_summary['items'],
            subtotal,
            cart_summary['delivery_fee'],
            self.user_data,
            tax_amount=tax  # Add tax parameter
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            order_details = dialog.get_order_details()
            self.confirm_and_place_order(order_details, cart_summary, tax)

    # MODIFICATION: Updated confirm_and_place_order and place_order methods
    # Add these methods to your CustomerWindow class (replace existing versions)

    def confirm_and_place_order(self, order_details, cart_summary, tax):
        """Show final confirmation before placing order with tax - DISPLAYS TAX"""
        QApplication.instance().setStyleSheet("""
            QMessageBox QLabel { color: black; }
            QMessageBox QPushButton { 
                color: black; 
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        items_text = "\n".join([f"• {item['name']} x{item['quantity']}" for item in cart_summary['items']])

        subtotal = cart_summary['subtotal']
        delivery_fee = cart_summary['delivery_fee']
        total = subtotal + tax + delivery_fee

        # MODIFIED: Added tax line to confirmation message
        confirmation_msg = (
            f"Please confirm your order:\n\n"
            f"Items:\n{items_text}\n\n"
            f"Subtotal: ₱{subtotal:.2f}\n"
            f"Tax (12% VAT): ₱{tax:.2f}\n"  # ADDED TAX LINE
            f"Delivery Fee: ₱{delivery_fee:.2f}\n"
            f"Total: ₱{total:.2f}\n\n"
            f"Delivery Address: {order_details['address']}\n"
            f"Payment Method: {order_details['payment_method']}\n"
        )

        if 'card_number' in order_details and order_details['card_number']:
            confirmation_msg += f"Card Number: {order_details['card_number']}\n"

        confirmation_msg += "\nProceed with this order?"

        reply = QMessageBox.question(
            self,
            'Confirm Order',
            confirmation_msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Add tax to order details
            order_details['tax'] = tax
            self.place_order(order_details)

    def place_order(self, order_details):
        """Place order using controller with tax - DISPLAYS TAX IN SUCCESS MESSAGE"""
        cart_summary = self.controller.get_cart_summary()
        subtotal = cart_summary['subtotal']
        tax = order_details.get('tax', 0)
        delivery_fee = cart_summary['delivery_fee']
        total = subtotal + tax + delivery_fee

        success, order_id, message = self.controller.place_order(order_details)

        if success:
            # MODIFIED: Added tax line to success message
            success_msg = (
                f'Your order #{order_id} has been placed!\n\n'
                f'Subtotal: ₱{subtotal:.2f}\n'
                f'Tax (12% VAT): ₱{tax:.2f}\n'  # ADDED TAX LINE
                f'Delivery Fee: ₱{delivery_fee:.2f}\n'
                f'Total: ₱{total:.2f}\n\n'
                f'Payment: {order_details["payment_method"]}\n'
            )

            if 'card_number' in order_details and order_details['card_number']:
                success_msg += f'Card: {order_details["card_number"]}\n'

            success_msg += (
                f'Delivery to: {order_details["address"]}\n\n'
                'Thank you for your order! You can track it in Order History.'
            )

            QApplication.instance().setStyleSheet("""
                QMessageBox QLabel { color: black; }
                QMessageBox QPushButton { 
                    color: black; 
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            QMessageBox.information(self, 'Order Placed Successfully!', success_msg)
            self.update_cart_display()
        else:
            QMessageBox.critical(self, 'Error', message)

    def show_order_history(self):
        """Show order history dialog"""
        dialog = OrderHistoryDialog(self, self.user_data['customer_id'], self.db_manager)
        dialog.exec()

    def logout(self):
        """Logout and return to login"""
        QApplication.instance().setStyleSheet("""
            QMessageBox QLabel { color: black; }
            QMessageBox QPushButton { 
                color: black; 
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        reply = QMessageBox.question(
            self,
            'Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                from Main.LoginWindow import LoginWindow
                self.login_window = LoginWindow(self.db_manager)
                self.login_window.show()
                self.close()
            except Exception as e:
                print(f"Logout error: {e}")
                QApplication.instance().setStyleSheet("QMessageBox QLabel { color: black; }")
                QMessageBox.critical(self, 'Error', f'Failed to logout: {str(e)}')

        #