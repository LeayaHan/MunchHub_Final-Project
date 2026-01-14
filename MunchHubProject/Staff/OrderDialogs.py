"""
OrderDialogs.py - Dialog classes for staff operations (View)
Place this file in: Staff/OrderDialogs.py
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class OrderAcceptDialog(QDialog):
    """Dialog for accepting orders"""

    def __init__(self, parent, order, controller):
        super().__init__(parent)
        self.order = order
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Accept Order - {self.order["OrderID"]}')
        self.setFixedSize(550, 450)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel(f"📦 Accept Order {self.order['OrderID']}")
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Order details
        details_frame = self.create_details_frame()
        layout.addWidget(details_frame)

        # Notes input
        notes_label = QLabel("Add Initial Notes (Optional):")
        notes_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        notes_label.setStyleSheet("color: #003274;")
        layout.addWidget(notes_label)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter any notes for this order...")
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QTextEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        layout.addWidget(self.notes_input)

        # Buttons
        button_layout = self.create_buttons()
        layout.addLayout(button_layout)

    def create_details_frame(self):
        """Create order details frame"""
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(10)

        def add_detail(label, value):
            h_layout = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #666;")
            val = QLabel(value)
            val.setFont(QFont('Arial', 10))
            val.setStyleSheet("color: #003274;")
            val.setWordWrap(True)
            h_layout.addWidget(lbl)
            h_layout.addWidget(val, 1)
            details_layout.addLayout(h_layout)

        total = float(self.order['TotalFee']) + float(self.order['DeliveryFee'])
        add_detail("Customer:", self.order['CustomerName'])
        add_detail("Items:", self.order['Items'])
        add_detail("Total:", f"₱{total:.2f}")
        add_detail("Address:", self.order['Address'])
        add_detail("Payment:", self.order['PaymentMethod'])

        return details_frame

    def create_buttons(self):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        cancel_btn.setFixedHeight(45)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        accept_btn = QPushButton('✓ Accept Order')
        accept_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        accept_btn.setFixedHeight(45)
        accept_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        accept_btn.clicked.connect(self.accept_order)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(accept_btn)

        return button_layout

    def accept_order(self):
        """Accept the order"""
        notes = self.notes_input.toPlainText().strip() or "Order confirmed and preparing"
        success, message = self.controller.accept_order(self.order['OrderID'], notes)

        if success:
            QMessageBox.information(
                self,
                'Success',
                f'Order {self.order["OrderID"]} has been accepted and is now preparing!'
            )
            self.accept()
        else:
            QMessageBox.critical(self, 'Error', f'Failed to accept order: {message}')


class TrackUpdateDialog(QDialog):
    """Dialog for updating order tracking"""

    def __init__(self, parent, track, controller):
        super().__init__(parent)
        self.track = track
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Update Track - {self.track["TrackID"]}')
        self.setFixedSize(500, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel(f"🔍 Update Tracking\n{self.track['TrackID']} - {self.track['OrderID']}")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Current info
        info_frame = self.create_info_frame()
        layout.addWidget(info_frame)

        # Status selection
        status_label = QLabel("New Status:")
        status_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        status_label.setStyleSheet("color: #003274;")
        layout.addWidget(status_label)

        self.status_combo = QComboBox()
        self.status_combo.addItems(['Confirmed', 'Preparing', 'Out for delivery'])
        self.status_combo.setCurrentText(self.track['Status'])
        self.status_combo.setFont(QFont('Arial', 11))
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                color: black;
                min-height: 35px;
            }
            QComboBox:focus {
                border: 2px solid #4CAF50;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
        """)
        layout.addWidget(self.status_combo)

        # Notes input
        notes_label = QLabel("Update Notes:")
        notes_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        notes_label.setStyleSheet("color: #003274;")
        layout.addWidget(notes_label)

        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(self.track['Notes'] or "")
        self.notes_input.setPlaceholderText("Enter tracking notes...")
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                color: black;
            }
            QTextEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        layout.addWidget(self.notes_input)

        # Buttons
        button_layout = self.create_buttons()
        layout.addLayout(button_layout)

    def create_info_frame(self):
        """Create current info frame"""
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)

        current_status = QLabel(f"Current Status: {self.track['Status']}")
        current_status.setFont(QFont('Arial', 10))
        current_status.setStyleSheet("color: black;")
        info_layout.addWidget(current_status)

        current_notes = QLabel(f"Current Notes: {self.track['Notes'] or 'None'}")
        current_notes.setFont(QFont('Arial', 10))
        current_notes.setStyleSheet("color: black;")
        current_notes.setWordWrap(True)
        info_layout.addWidget(current_notes)

        return info_frame

    def create_buttons(self):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        cancel_btn.setFixedHeight(45)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        update_btn = QPushButton('✓ Update')
        update_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        update_btn.setFixedHeight(45)
        update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        update_btn.clicked.connect(self.update_track)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(update_btn)

        return button_layout

    def update_track(self):
        """Update tracking record"""
        new_status = self.status_combo.currentText()
        new_notes = self.notes_input.toPlainText().strip()

        success, message = self.controller.update_track(
            self.track['TrackID'],
            new_status,
            new_notes
        )

        if success:
            QMessageBox.information(
                self,
                'Success',
                f'Tracking record {self.track["TrackID"]} has been updated!'
            )
            self.accept()
        else:
            QMessageBox.critical(self, 'Error', f'Failed to update tracking: {message}')