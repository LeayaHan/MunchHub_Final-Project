from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCharts import *


class StatCard(QFrame):
    """Statistics card widget"""

    def __init__(self, icon, title, value, color):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Arial', 40))
        icon_label.setStyleSheet(f"color: {color};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #000000;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 12))
        title_label.setStyleSheet("color: #000000;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)


from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCharts import *


class SalesChart(QChartView):
    """Sales bar chart widget"""

    def __init__(self, sales_data):
        super().__init__()

        # Create bar set
        bar_set = QBarSet("Monthly Sales (₱)")

        # Add data points
        months = list(sales_data.keys())
        for month in months:
            bar_set.append(sales_data[month])

        # Style the bars
        bar_set.setColor(QColor("#2196F3"))  # Blue color for bars
        bar_set.setBorderColor(QColor("#1976D2"))  # Darker blue border

        # Create bar series
        series = QBarSeries()
        series.append(bar_set)

        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Sales Overview")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # Create X axis (categories - months)
        axis_x = QBarCategoryAxis()
        axis_x.append(months)
        axis_x.setTitleText("Months")
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        # Create Y axis (values)
        axis_y = QValueAxis()
        max_value = max(sales_data.values()) if sales_data.values() else 1000
        axis_y.setRange(0, max_value * 1.2)
        axis_y.setTitleText("Sales Amount (₱)")
        axis_y.setLabelFormat("%.0f")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Chart styling
        chart.setBackgroundBrush(QBrush(QColor("#ffffff")))
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Set chart to view
        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMinimumHeight(400)

        # Style the view
        self.setStyleSheet("""
            QChartView {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e6e6e6;
            }
        """)


class StyledTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #000000;
                gridline-color: #e0e0e0;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #003274;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                color: #000000;
                padding: 6px;
            }

            QTableWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }

            QTableWidget::item:hover {
                background-color: #E3F2FD;
            }
        """)

        self.setAlternatingRowColors(True)
        self.setStyleSheet(self.styleSheet() + """
            QTableWidget {
                alternate-background-color: #f9f9f9;
            }
        """)

        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Make table read-only (not editable)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


class ActionButton(QPushButton):
    """Styled action button"""

    def __init__(self, text, color, icon=""):
        super().__init__(f"{icon} {text}" if icon else text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def darken_color(self, hex_color):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"


def get_input_style():
    """Get consistent input field styling"""
    return """
        QLineEdit, QComboBox, QTextEdit {
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 13px;
            background-color: white;
        }
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
            border: 2px solid #003274;
        }
    """