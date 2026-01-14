"""
MenuWidgets.py - Menu and Cart Item Widgets with Tax Display
MODIFICATIONS:
1. Added tax indication to menu items (prices shown are before tax)
2. Fixed Add to Cart signal connection
3. Added visual feedback when adding items
4. Changed CartItemWidget background to white with explicit styling
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class MenuItemWidget(QWidget):
    """Widget for displaying a menu item with add to cart button"""

    # Signal emitted when item is added to cart
    item_added = pyqtSignal(dict)

    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.initUI()

    def initUI(self):
        """Initialize the menu item UI"""
        self.setFixedHeight(130)  # Increased for tax note
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #e0e0e0;
            }
            QWidget:hover {
                border: 2px solid #ffbd59;
                background-color: #fffef8;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # Left side - Item details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(5)

        # Item name
        name_label = QLabel(self.item_data['ItemName'])
        name_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #003274; border: none;")
        details_layout.addWidget(name_label)

        # Price before tax
        price = float(self.item_data['Price'])
        price_label = QLabel(f"₱{price:.2f}")
        price_label.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        price_label.setStyleSheet("color: #ff9800; border: none;")
        details_layout.addWidget(price_label)

        # Tax note
        tax_note = QLabel('(+12% tax at checkout)')
        tax_note.setFont(QFont('Arial', 9))
        tax_note.setStyleSheet("color: #999; border: none; font-style: italic;")
        details_layout.addWidget(tax_note)

        # Availability status
        if self.item_data.get('isAvailable', 1) == 1:
            status_label = QLabel('✓ Available')
            status_label.setStyleSheet("color: #4CAF50; font-size: 11px; border: none;")
        else:
            status_label = QLabel('✗ Out of Stock')
            status_label.setStyleSheet("color: #F44336; font-size: 11px; border: none;")
        details_layout.addWidget(status_label)

        details_layout.addStretch()
        layout.addLayout(details_layout, 1)

        # Right side - Add to cart button
        self.add_button = QPushButton('Add to Cart')
        self.add_button.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.add_button.setFixedSize(130, 45)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Disable button if not available
        is_available = self.item_data.get('isAvailable', 1) == 1
        self.add_button.setEnabled(is_available)

        if is_available:
            self.add_button.setStyleSheet("""
                QPushButton {
                    background-color: #003274;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #004a9e;
                }
                QPushButton:pressed {
                    background-color: #002052;
                }
            """)
        else:
            self.add_button.setStyleSheet("""
                QPushButton {
                    background-color: #cccccc;
                    color: #666666;
                    border: none;
                    border-radius: 8px;
                }
            """)

        # CRITICAL: Connect the button click to emit signal
        self.add_button.clicked.connect(self.on_add_clicked)

        layout.addWidget(self.add_button)

    def on_add_clicked(self):
        """Handle add to cart button click"""
        # Emit signal with item data
        self.item_added.emit(self.item_data)

        # Visual feedback
        self.add_button.setText('Added!')
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
        """)

        # Reset button after 1 second
        QTimer.singleShot(1000, self.reset_button)

    def reset_button(self):
        """Reset button to original state"""
        self.add_button.setText('Add to Cart')
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #003274;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004a9e;
            }
            QPushButton:pressed {
                background-color: #002052;
            }
        """)


class CartItemWidget(QWidget):
    """Widget for displaying a cart item with quantity controls - WHITE BACKGROUND"""

    # Signals
    quantity_changed = pyqtSignal(dict, int)  # cart_item, change_amount
    item_removed = pyqtSignal(dict)  # cart_item

    def __init__(self, cart_item, parent=None):
        super().__init__(parent)
        self.cart_item = cart_item
        self.initUI()

    def initUI(self):
        """Initialize the cart item UI with white background"""
        self.setFixedHeight(100)

        # Force white background with !important equivalent by using object name
        self.setObjectName("cartItem")
        self.setStyleSheet("""
            #cartItem {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #e0e0e0;
            }
        """)

        # Create a white inner container to ensure white background
        container = QWidget()
        container.setStyleSheet("background-color: white; border-radius: 10px;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        # Top row - Name and remove button
        top_layout = QHBoxLayout()

        name_label = QLabel(self.cart_item['name'])
        name_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #003274; border: none; background-color: transparent;")
        name_label.setWordWrap(True)
        top_layout.addWidget(name_label, 1)

        # Remove button
        remove_btn = QPushButton('✕')
        remove_btn.setFixedSize(25, 25)
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        remove_btn.clicked.connect(lambda: self.item_removed.emit(self.cart_item))
        top_layout.addWidget(remove_btn)

        layout.addLayout(top_layout)

        # Bottom row - Price, quantity controls, subtotal
        bottom_layout = QHBoxLayout()

        # Price per item
        price_label = QLabel(f"₱{self.cart_item['price']:.2f}")
        price_label.setFont(QFont('Arial', 10))
        price_label.setStyleSheet("color: #666; border: none; background-color: transparent;")
        bottom_layout.addWidget(price_label)

        bottom_layout.addStretch()

        # Quantity controls
        qty_container = QWidget()
        qty_container.setStyleSheet("background-color: transparent; border: none;")
        qty_layout = QHBoxLayout(qty_container)
        qty_layout.setContentsMargins(0, 0, 0, 0)
        qty_layout.setSpacing(8)

        # Decrease button
        minus_btn = QPushButton('−')
        minus_btn.setFixedSize(30, 30)
        minus_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        minus_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        minus_btn.clicked.connect(lambda: self.quantity_changed.emit(self.cart_item, -1))
        qty_layout.addWidget(minus_btn)

        # Quantity display
        self.qty_label = QLabel(str(self.cart_item['quantity']))
        self.qty_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.qty_label.setStyleSheet("color: #003274; border: none; background-color: transparent;")
        self.qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qty_label.setFixedWidth(30)
        qty_layout.addWidget(self.qty_label)

        # Increase button
        plus_btn = QPushButton('+')
        plus_btn.setFixedSize(30, 30)
        plus_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        plus_btn.setStyleSheet("""
            QPushButton {
                background-color: #003274;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004a9e;
            }
        """)
        plus_btn.clicked.connect(lambda: self.quantity_changed.emit(self.cart_item, 1))
        qty_layout.addWidget(plus_btn)

        bottom_layout.addWidget(qty_container)

        bottom_layout.addStretch()

        # Subtotal
        subtotal_label = QLabel(f"₱{self.cart_item['subtotal']:.2f}")
        subtotal_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        subtotal_label.setStyleSheet("color: #ffbd59; border: none; background-color: transparent;")
        bottom_layout.addWidget(subtotal_label)

        layout.addLayout(bottom_layout)

        main_layout.addWidget(container)