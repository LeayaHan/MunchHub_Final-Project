"""
SalesGraphView.py - Interactive Sales Graph with Day/Month/Year filtering
Place this file in your Admin folder
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SalesGraphView(QWidget):
    """View for displaying sales graphs with filtering options"""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.current_view = 'month'  # Default view
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.initUI()
        self.load_data()

    def initUI(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header with title and controls
        header = self.create_header()
        layout.addWidget(header)

        # Graph container
        self.graph_container = QWidget()
        self.graph_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.graph_container.setGraphicsEffect(shadow)

        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(30, 30, 30, 30)
        self.graph_container.setLayout(graph_layout)

        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)

        layout.addWidget(self.graph_container)

    def create_header(self):
        """Create header with controls"""
        header = QWidget()
        header.setStyleSheet("background-color: transparent;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header.setLayout(header_layout)

        # Title
        title = QLabel("Sales Analytics")
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #003274;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # View selector buttons
        view_label = QLabel("View by:")
        view_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        view_label.setStyleSheet("color: #003274;")
        header_layout.addWidget(view_label)

        # Button group for view selection
        self.day_btn = self.create_view_button("Day")
        self.month_btn = self.create_view_button("Month")
        self.year_btn = self.create_view_button("Year")

        self.day_btn.clicked.connect(lambda: self.change_view('day'))
        self.month_btn.clicked.connect(lambda: self.change_view('month'))
        self.year_btn.clicked.connect(lambda: self.change_view('year'))

        header_layout.addWidget(self.day_btn)
        header_layout.addWidget(self.month_btn)
        header_layout.addWidget(self.year_btn)

        header_layout.addSpacing(20)

        # Year selector
        year_label = QLabel("Year:")
        year_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        year_label.setStyleSheet("color: #003274;")
        header_layout.addWidget(year_label)

        self.year_combo = QComboBox()
        self.year_combo.setFont(QFont('Arial', 11))
        self.year_combo.setMinimumWidth(100)
        self.year_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #003274;
                border-radius: 8px;
                background-color: white;
                color: #003274;
            }
            QComboBox:hover {
                background-color: #f0f0f0;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #003274;
                selection-background-color: #ffbd59;
                selection-color: #003274;
            }
        """)

        # Populate years (from 2020 to current year + 1)
        current_year = datetime.now().year
        for year in range(2020, current_year + 2):
            self.year_combo.addItem(str(year), year)
        self.year_combo.setCurrentText(str(self.current_year))
        self.year_combo.currentIndexChanged.connect(self.on_year_changed)

        header_layout.addWidget(self.year_combo)

        # Month selector (initially hidden)
        self.month_label = QLabel("Month:")
        self.month_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.month_label.setStyleSheet("color: #003274;")
        header_layout.addWidget(self.month_label)

        self.month_combo = QComboBox()
        self.month_combo.setFont(QFont('Arial', 11))
        self.month_combo.setMinimumWidth(120)
        self.month_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #003274;
                border-radius: 8px;
                background-color: white;
                color: #003274;
            }
            QComboBox:hover {
                background-color: #f0f0f0;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #003274;
                selection-background-color: #ffbd59;
                selection-color: #003274;
            }
        """)

        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        for i, month in enumerate(months, 1):
            self.month_combo.addItem(month, i)
        self.month_combo.setCurrentIndex(self.current_month - 1)
        self.month_combo.currentIndexChanged.connect(self.on_month_changed)

        header_layout.addWidget(self.month_combo)

        # Initially hide month selector (shown only for day view)
        self.month_label.hide()
        self.month_combo.hide()

        header_layout.addSpacing(20)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd59;
                color: #003274;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #ffa726;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(refresh_btn)

        return header

    def create_view_button(self, text):
        """Create a view selector button"""
        btn = QPushButton(text)
        btn.setFont(QFont('Arial', 11))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumSize(80, 40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #003274;
                border: 2px solid #003274;
                border-radius: 8px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        return btn

    def set_active_button(self, active_btn):
        """Set the active view button"""
        for btn in [self.day_btn, self.month_btn, self.year_btn]:
            if btn == active_btn:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #003274;
                        color: white;
                        border: 2px solid #003274;
                        border-radius: 8px;
                        padding: 8px 15px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: #003274;
                        border: 2px solid #003274;
                        border-radius: 8px;
                        padding: 8px 15px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """)

    def change_view(self, view):
        """Change the view type"""
        self.current_view = view

        # Update active button
        if view == 'day':
            self.set_active_button(self.day_btn)
            self.month_label.show()
            self.month_combo.show()
        elif view == 'month':
            self.set_active_button(self.month_btn)
            self.month_label.hide()
            self.month_combo.hide()
        else:  # year
            self.set_active_button(self.year_btn)
            self.month_label.hide()
            self.month_combo.hide()

        self.load_data()

    def on_year_changed(self, index):
        """Handle year change"""
        self.current_year = self.year_combo.itemData(index)
        self.load_data()

    def on_month_changed(self, index):
        """Handle month change"""
        self.current_month = self.month_combo.itemData(index)
        self.load_data()

    def load_data(self):
        """Load and display sales data"""
        # Set initial active button
        if self.current_view == 'day':
            self.set_active_button(self.day_btn)
        elif self.current_view == 'month':
            self.set_active_button(self.month_btn)
        else:
            self.set_active_button(self.year_btn)

        if self.current_view == 'day':
            self.load_daily_sales()
        elif self.current_view == 'month':
            self.load_monthly_sales()
        else:
            self.load_yearly_sales()

    def load_daily_sales(self):
        """Load sales by day for a specific month"""
        data = self.controller.get_daily_sales(self.current_year, self.current_month)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, 'No sales data available for this month',
                    ha='center', va='center', fontsize=14, color='#666')
            self.canvas.draw()
            return

        days = [item['day'] for item in data]
        sales = [float(item['total_sales']) for item in data]

        # Create bar chart
        bars = ax.bar(days, sales, color='#003274', alpha=0.8, edgecolor='#002050', linewidth=1.5)

        # Customize chart
        month_name = datetime(self.current_year, self.current_month, 1).strftime('%B')
        ax.set_title(f'Daily Sales - {month_name} {self.current_year}',
                     fontsize=16, fontweight='bold', color='#003274', pad=20)
        ax.set_xlabel('Day of Month', fontsize=12, fontweight='bold', color='#003274')
        ax.set_ylabel('Sales (₱)', fontsize=12, fontweight='bold', color='#003274')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'₱{height:,.0f}',
                    ha='center', va='bottom', fontsize=9, color='#003274')

        self.figure.tight_layout()
        self.canvas.draw()

    def load_monthly_sales(self):
        """Load sales by month for a specific year"""
        data = self.controller.get_monthly_sales_by_year(self.current_year)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, 'No sales data available for this year',
                    ha='center', va='center', fontsize=14, color='#666')
            self.canvas.draw()
            return

        months = [datetime(2000, item['month'], 1).strftime('%b') for item in data]
        sales = [float(item['total_sales']) for item in data]

        # Create bar chart with gradient effect
        bars = ax.bar(months, sales, color='#003274', alpha=0.8, edgecolor='#002050', linewidth=1.5)

        # Customize chart
        ax.set_title(f'Monthly Sales - {self.current_year}',
                     fontsize=16, fontweight='bold', color='#003274', pad=20)
        ax.set_xlabel('Month', fontsize=12, fontweight='bold', color='#003274')
        ax.set_ylabel('Sales (₱)', fontsize=12, fontweight='bold', color='#003274')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'₱{height:,.0f}',
                    ha='center', va='bottom', fontsize=9, color='#003274')

        # Rotate x-axis labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)

        self.figure.tight_layout()
        self.canvas.draw()

    def load_yearly_sales(self):
        """Load sales by year"""
        data = self.controller.get_yearly_sales()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, 'No sales data available',
                    ha='center', va='center', fontsize=14, color='#666')
            self.canvas.draw()
            return

        years = [str(item['year']) for item in data]
        sales = [float(item['total_sales']) for item in data]

        # Create bar chart
        bars = ax.bar(years, sales, color='#003274', alpha=0.8, edgecolor='#002050', linewidth=1.5)

        # Customize chart
        ax.set_title('Yearly Sales Comparison',
                     fontsize=16, fontweight='bold', color='#003274', pad=20)
        ax.set_xlabel('Year', fontsize=12, fontweight='bold', color='#003274')
        ax.set_ylabel('Sales (₱)', fontsize=12, fontweight='bold', color='#003274')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'₱{height:,.0f}',
                    ha='center', va='bottom', fontsize=10, color='#003274', fontweight='bold')

        self.figure.tight_layout()
        self.canvas.draw()