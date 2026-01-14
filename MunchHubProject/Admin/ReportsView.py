from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Admin.AdminComponents import SalesChart
from Tools.Utility import ReportGenerator
from datetime import datetime


class ReportsView(QWidget):
    """Reports View - Display sales chart and export functionality"""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.report_generator = ReportGenerator(controller)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("Business Reports")
        title_label.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Export button
        export_btn = QPushButton("Export to PDF")
        export_btn.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setMinimumHeight(40)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        export_btn.clicked.connect(self.export_report)
        header_layout.addWidget(export_btn)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFont(QFont('Arial', 12, QFont.Weight.Bold))
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
        refresh_btn.clicked.connect(self.load_reports)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Date range selector
        date_range_layout = QHBoxLayout()

        date_label = QLabel("Report Period:")
        date_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        date_label.setStyleSheet("color: #000000;")
        date_range_layout.addWidget(date_label)

        self.period_combo = QComboBox()
        self.period_combo.setMinimumHeight(40)
        self.period_combo.addItems([
            "Today",
            "This Week",
            "This Month",
            "This Year",
            "All Time"
        ])
        self.period_combo.setCurrentText("This Month")
        self.period_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                color: black;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 13px;
                min-width: 150px;
                background-color: white;
            }
        """)
        self.period_combo.currentTextChanged.connect(self.load_reports)
        date_range_layout.addWidget(self.period_combo)

        date_range_layout.addStretch()
        layout.addLayout(date_range_layout)

        # Sales chart section with centered header
        chart_header_layout = QHBoxLayout()
        chart_header_layout.addStretch()

        chart_title = QLabel("MONTHLY SALES PERFORMANCE")
        chart_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        chart_title.setStyleSheet("""
            color: white;
            background-color: #1e3a5f;
            padding: 15px 40px;
            border-radius: 8px;
        """)
        chart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_header_layout.addWidget(chart_title)

        chart_header_layout.addStretch()
        layout.addLayout(chart_header_layout)

        # Sales chart widget (framed container)
        self.chart_container = QFrame()
        self.chart_container.setObjectName("chartContainer")
        self.chart_container.setStyleSheet("""
            QFrame#chartContainer {
                background-color: #ffffff;
                border: 1px solid #e6e6e6;
                border-radius: 12px;
            }
        """)

        self.chart_layout = QVBoxLayout()
        self.chart_layout.setContentsMargins(18, 18, 18, 18)
        self.chart_layout.setSpacing(0)
        self.chart_container.setLayout(self.chart_layout)

        self.chart_container.setMinimumHeight(400)
        layout.addWidget(self.chart_container)

        # Info label
        info_label = QLabel("Export to PDF to view detailed KPIs and business insights")
        info_label.setFont(QFont('Arial', 11))
        info_label.setStyleSheet("""
            color: #666666;
            background-color: #f5f5f5;
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        layout.addStretch()

        # Load initial data
        self.load_reports()

    def load_reports(self):
        """Load and display sales chart"""
        try:
            # Clear existing chart
            self.clear_container(self.chart_layout)

            # Create sales chart (pass show_title=False if SalesChart supports it)
            sales_data = self.controller.get_monthly_sales()
            sales_chart = SalesChart(sales_data)
            sales_chart.setMinimumHeight(360)
            sales_chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.chart_layout.addWidget(sales_chart)

        except Exception as e:
            self.show_message("Error", f"Error loading reports: {e}", "critical")
            import traceback
            traceback.print_exc()

    def clear_container(self, layout):
        """Clear all widgets from a layout"""
        if isinstance(layout, QHBoxLayout) or isinstance(layout, QVBoxLayout):
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

    def export_report(self):
        """Export report to PDF using ReportLab"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report as PDF",
            f"MunchHub_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path:
            try:
                # Ensure file has .pdf extension
                if not file_path.lower().endswith('.pdf'):
                    file_path += '.pdf'

                # Get report period
                period = self.period_combo.currentText()

                # Get sales data for the chart
                sales_data = self.controller.get_monthly_sales()

                # Generate PDF using ReportGenerator with chart data
                success = self.report_generator.generate_pdf(file_path, period, sales_data)

                if success:
                    self.show_message(
                        "Export Successful",
                        f"Report successfully exported to:\n{file_path}",
                        "information"
                    )
                else:
                    self.show_message(
                        "Export Failed",
                        "Failed to export report. Please check console for errors.",
                        "critical"
                    )

            except Exception as e:
                self.show_message(
                    "Export Failed",
                    f"Failed to export report:\n{str(e)}",
                    "critical"
                )
                import traceback
                traceback.print_exc()

    def apply_message_box_style(self):
        """Apply black text styling to message boxes"""
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

    def show_message(self, title, message, msg_type):
        """Show message box with proper styling"""
        self.apply_message_box_style()

        if msg_type == "information":
            QMessageBox.information(self, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self, title, message)
        elif msg_type == "critical":
            QMessageBox.critical(self, title, message)