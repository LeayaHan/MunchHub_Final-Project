"""
TrackOrdersPage.py - Track Orders Page (View)
Place this file in: Staff/TrackOrdersPage.py
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Staff.OrderDialogs import TrackUpdateDialog


class TrackOrdersPage(QWidget):
    """Page for tracking orders"""

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

        # Track table
        self.track_table = self.create_track_table()
        layout.addWidget(self.track_table)

    def create_header(self):
        """Create page header"""
        header_layout = QHBoxLayout()

        title = QLabel("Track Orders")
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

    def create_track_table(self):
        """Create track table"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Track ID", "Order ID", "Status", "Notes", "Update Date", "Action"
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
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(60)

        return table

    def load_data(self):
        """Load track orders"""
        tracks = self.controller.get_track_orders()
        self.populate_table(tracks)

    def populate_table(self, tracks):
        """Populate table with tracking records"""
        self.track_table.setRowCount(len(tracks) if tracks else 1)

        if not tracks:
            empty_msg = QTableWidgetItem("No tracking records found")
            empty_msg.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_msg.setForeground(QColor('#999'))
            empty_msg.setFlags(empty_msg.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.track_table.setItem(0, 0, empty_msg)
            self.track_table.setSpan(0, 0, 1, 6)
            return

        status_colors = {
            'Confirmed': '#4CAF50',
            'Preparing': '#2196F3',
            'Out for delivery': '#9C27B0'
        }

        for row, track in enumerate(tracks):
            # Track ID
            track_id_item = QTableWidgetItem(track['TrackID'])
            track_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            track_id_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            track_id_item.setForeground(QColor('#003274'))
            track_id_item.setFlags(track_id_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.track_table.setItem(row, 0, track_id_item)

            # Order ID
            order_item = QTableWidgetItem(track['OrderID'])
            order_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            order_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            order_item.setForeground(QColor('#003274'))
            order_item.setFlags(order_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.track_table.setItem(row, 1, order_item)

            # Status
            status_item = QTableWidgetItem(track['Status'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            status_item.setForeground(QColor(status_colors.get(track['Status'], '#666')))
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.track_table.setItem(row, 2, status_item)

            # Notes
            notes_item = QTableWidgetItem(track['Notes'] or "—")
            notes_item.setForeground(QColor('black'))
            notes_item.setFlags(notes_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.track_table.setItem(row, 3, notes_item)

            # Update Date
            date_str = track['UpdateDate'].strftime('%b %d, %Y %I:%M %p')
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setForeground(QColor('black'))
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.track_table.setItem(row, 4, date_item)

            # Action button
            action_widget = self.create_action_button(track)
            self.track_table.setCellWidget(row, 5, action_widget)

    def create_action_button(self, track):
        """Create update button"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        update_btn = QPushButton("Update")
        update_btn.setFixedSize(90, 30)
        update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        update_btn.clicked.connect(lambda: self.update_track(track))

        layout.addWidget(update_btn)

        return widget

    def update_track(self, track):
        """Open update track dialog"""
        dialog = TrackUpdateDialog(self, track, self.controller)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def showEvent(self, event):
        """Apply global message box styling when page is shown"""
        super().showEvent(event)
        # Set global stylesheet for message boxes
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