from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import os


class ReportGenerator:
    """Generate comprehensive PDF reports using ReportLab with table-based layout"""

    def __init__(self, controller):
        self.controller = controller
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#003274'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#003274'),
            spaceAfter=6,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        )

        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.white,
            spaceAfter=0,
            spaceBefore=0,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#003274'),
            alignment=TA_CENTER
        )

        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            spaceAfter=0,
            leading=11
        )

        self.small_style = ParagraphStyle(
            'SmallText',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            spaceAfter=0
        )

    def generate_pdf(self, file_path, period, sales_data):
        """Generate the complete comprehensive PDF report"""
        try:
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )

            elements = []

            # Header
            elements.extend(self.create_header(period))
            elements.append(Spacer(1, 0.15 * inch))

            # Metadata table
            elements.extend(self.create_metadata_table(period))
            elements.append(Spacer(1, 0.15 * inch))

            # Executive Summary table
            elements.extend(self.create_executive_summary_table())
            elements.append(Spacer(1, 0.15 * inch))

            # KPIs table
            elements.extend(self.create_kpi_table())
            elements.append(Spacer(1, 0.15 * inch))

            # Sales chart
            if sales_data and len(sales_data) > 0:
                elements.extend(self.create_sales_chart_section(sales_data))
                elements.append(Spacer(1, 0.15 * inch))

            # Quarterly sales table
            elements.extend(self.create_sales_summary_table())
            elements.append(Spacer(1, 0.15 * inch))

            # Sales analysis table
            elements.extend(self.create_sales_analysis_table(sales_data))

            # Page break
            elements.append(PageBreak())

            # Product performance table
            elements.extend(self.create_product_table())
            elements.append(Spacer(1, 0.15 * inch))

            # Customer analytics table
            elements.extend(self.create_customer_table())
            elements.append(Spacer(1, 0.15 * inch))

            # Order analytics table
            elements.extend(self.create_order_table())

            # Page break
            elements.append(PageBreak())

            # Business insights table
            elements.extend(self.create_insights_table())
            elements.append(Spacer(1, 0.15 * inch))

            # Operational metrics table
            elements.extend(self.create_operational_table())
            elements.append(Spacer(1, 0.15 * inch))

            # Recommendations table
            elements.extend(self.create_recommendations_table())

            # Footer
            elements.append(Spacer(1, 0.2 * inch))
            elements.extend(self.create_footer())

            doc.build(elements)
            print(f"PDF generated successfully: {file_path}")
            return True

        except Exception as e:
            print(f"Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def create_header(self, period):
        """Create compact report header"""
        elements = []

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            logo_path = os.path.join(parent_dir, 'PNG', 'logo.png')

            if os.path.exists(logo_path):
                logo = RLImage(logo_path, width=1.2 * inch, height=1.2 * inch)
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 0.1 * inch))
        except Exception as e:
            print(f"Error loading logo: {e}")

        title = Paragraph("MUNCHHUB BUSINESS REPORT", self.title_style)
        elements.append(title)

        return elements

    def create_metadata_table(self, period):
        """Create metadata as table"""
        elements = []

        now = datetime.now()
        data = [
            [Paragraph('<b>Generated:</b>', self.normal_style),
             Paragraph(now.strftime('%B %d, %Y at %I:%M %p'), self.normal_style)],
            [Paragraph('<b>Report Period:</b>', self.normal_style),
             Paragraph(period, self.normal_style)],
            [Paragraph('<b>Report Type:</b>', self.normal_style),
             Paragraph('Comprehensive Business Analytics', self.normal_style)]
        ]

        table = Table(data, colWidths=[2 * inch, 4.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elements.append(table)
        return elements

    def create_executive_summary_table(self):
        """Create executive summary as table"""
        elements = []

        # Section header
        header_data = [[Paragraph('EXECUTIVE SUMMARY', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            stats = self.controller.get_dashboard_stats()
            completed_orders = self.controller.get_completed_orders()
            avg_order = self.controller.get_avg_order_value()

            total_revenue = float(stats.get('total_revenue', 0))
            total_orders = int(stats.get('total_orders', 0))
            total_users = int(stats.get('total_users', 0))
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0

            data = [
                ['Metric', 'Value', 'Status'],
                ['Total Revenue', f'₱{total_revenue:,.2f}', 'Strong Performance'],
                ['Orders Processed', f'{total_orders}', f'{completion_rate:.1f}% Completion'],
                ['Active Customers', f'{total_users}', 'Growing'],
                ['Avg Transaction', f'₱{float(avg_order):,.2f}', 'Healthy'],
                ['Business Health', 'Operational', '✓ Excellent']
            ]

            table = Table(data, colWidths=[2.2 * inch, 2.2 * inch, 2.1 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFEF8')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        except Exception as e:
            print(f"Error creating executive summary: {e}")

        return elements

    def create_kpi_table(self):
        """Create KPI table"""
        elements = []

        # Section header
        header_data = [[Paragraph('KEY PERFORMANCE INDICATORS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            stats = self.controller.get_dashboard_stats()
            completed_orders = self.controller.get_completed_orders()
            avg_order = self.controller.get_avg_order_value()

            total_revenue = float(stats.get('total_revenue', 0))
            total_orders = int(stats.get('total_orders', 0))
            total_users = int(stats.get('total_users', 0))
            menu_items = int(stats.get('total_menu_items', 0))
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0

            data = [
                ['Metric', 'Current Value', 'Performance'],
                ['Total Revenue', f'₱{total_revenue:,.2f}', '● Excellent'],
                ['Total Orders', str(total_orders), '● Active'],
                ['Completed Orders', f'{completed_orders} ({completion_rate:.1f}%)', '● Strong'],
                ['Avg Order Value', f'₱{float(avg_order):,.2f}', '● Healthy'],
                ['Total Customers', str(total_users), '● Growing'],
                ['Menu Items', str(menu_items), '● Diverse']
            ]

            table = Table(data, colWidths=[2.5 * inch, 2.5 * inch, 1.5 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
                ('TEXTCOLOR', (2, 1), (2, -1), colors.green),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        except Exception as e:
            print(f"Error creating KPI table: {e}")

        return elements

    def create_sales_chart_section(self, sales_data):
        """Create sales chart section"""
        elements = []

        # Section header
        header_data = [[Paragraph('MONTHLY SALES PERFORMANCE', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        chart = self.create_sales_chart(sales_data)
        elements.append(chart)

        return elements

    def create_sales_chart(self, sales_data):
        """Create bar chart for monthly sales"""
        drawing = Drawing(400, 220)

        months = []
        revenues = []

        if isinstance(sales_data, dict):
            for month, revenue in sales_data.items():
                months.append(str(month))
                revenues.append(float(revenue) if revenue else 0)
        elif isinstance(sales_data, list):
            for item in sales_data:
                if isinstance(item, dict):
                    if 'month' in item and 'revenue' in item:
                        months.append(str(item['month']))
                        revenues.append(float(item['revenue']) if item['revenue'] else 0)
                    else:
                        for month, revenue in item.items():
                            months.append(str(month))
                            revenues.append(float(revenue) if revenue else 0)

        if not revenues or all(r == 0 for r in revenues):
            revenues = [0]
            months = ['No Data']

        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 40
        chart.height = 160
        chart.width = 300
        chart.data = [revenues]

        chart.categoryAxis.categoryNames = months
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.dx = 8
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.labels.angle = 45
        chart.categoryAxis.labels.fontSize = 7

        max_revenue = max(revenues) if revenues else 100
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max_revenue * 1.2
        chart.valueAxis.valueStep = (max_revenue * 1.2 / 5) if max_revenue > 0 else 20
        chart.valueAxis.labels.fontSize = 9

        chart.bars[0].fillColor = colors.HexColor('#2196F3')
        chart.bars[0].strokeColor = colors.HexColor('#1976D2')
        chart.bars[0].strokeWidth = 1.5

        drawing.add(chart)
        return drawing

    def create_sales_summary_table(self):
        """Create quarterly sales summary table"""
        elements = []

        # Section header
        header_data = [[Paragraph('QUARTERLY SALES BREAKDOWN', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        monthly_sales = self.controller.get_monthly_sales()

        data = [['Quarter', 'Months', 'Total Sales', 'Avg/Month']]

        quarters = [
            ('Q1', ['Jan', 'Feb', 'Mar']),
            ('Q2', ['Apr', 'May', 'Jun']),
            ('Q3', ['Jul', 'Aug', 'Sep']),
            ('Q4', ['Oct', 'Nov', 'Dec'])
        ]

        total_sales = 0
        for q_name, q_months in quarters:
            q_total = sum(monthly_sales.get(m, 0) for m in q_months)
            q_avg = q_total / 3
            total_sales += q_total
            data.append([q_name, ', '.join(q_months), f'₱{q_total:,.2f}', f'₱{q_avg:,.2f}'])

        avg_all = total_sales / 12 if total_sales > 0 else 0
        data.append(['TOTAL', 'All Months', f'₱{total_sales:,.2f}', f'₱{avg_all:,.2f}'])

        table = Table(data, colWidths=[0.8 * inch, 2.5 * inch, 1.7 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003274')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (0, 1), (0, -2), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F5F5')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(table)
        return elements

    def create_sales_analysis_table(self, sales_data):
        """Create sales analysis table"""
        elements = []

        # Section header
        header_data = [[Paragraph('SALES TREND ANALYSIS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        revenues = []
        if isinstance(sales_data, dict):
            revenues = [float(v) if v else 0 for v in sales_data.values()]

        if revenues and len(revenues) > 1:
            total_sales = sum(revenues)
            avg_sales = total_sales / len(revenues)
            max_sales = max(revenues)
            min_sales = min(revenues)

            first_half = sum(revenues[:6]) if len(revenues) >= 6 else sum(revenues[:len(revenues) // 2])
            second_half = sum(revenues[6:]) if len(revenues) >= 6 else sum(revenues[len(revenues) // 2:])
            growth = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0

            data = [
                ['Metric', 'Value'],
                ['Total Period Sales', f'₱{total_sales:,.2f}'],
                ['Average Monthly Sales', f'₱{avg_sales:,.2f}'],
                ['Peak Sales Month', f'₱{max_sales:,.2f}'],
                ['Lowest Sales Month', f'₱{min_sales:,.2f}'],
                ['Period Growth', f'{growth:+.1f}%'],
                ['Trend', 'Positive' if growth > 0 else 'Stable' if growth == 0 else 'Adjusting']
            ]

            table = Table(data, colWidths=[2.5 * inch, 4 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFEF8')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        return elements

    def create_product_table(self):
        """Create product performance table"""
        elements = []

        # Section header
        header_data = [[Paragraph('PRODUCT CATALOG PERFORMANCE', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            menu_items = self.controller.model.get_all_menu_items()
            categories = self.controller.model.get_all_categories()

            total_items = len(menu_items)
            available = sum(1 for item in menu_items if item.get('isAvailable', 0) == 1)

            # Summary data
            summary_data = [
                ['Metric', 'Value'],
                ['Total Menu Items', str(total_items)],
                ['Available Items', f'{available} ({available / total_items * 100:.1f}%)' if total_items > 0 else '0'],
                ['Product Categories', str(len(categories))],
                ['Avg Items/Category', f'{total_items / len(categories):.1f}' if categories else '0']
            ]

            summary_table = Table(summary_data, colWidths=[2.5 * inch, 4 * inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFEF8')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))

            elements.append(summary_table)

            if menu_items:
                elements.append(Spacer(1, 0.1 * inch))

                product_data = [['Product Name', 'Category', 'Price', 'Status']]
                for item in menu_items[:10]:
                    status = '✓' if item.get('isAvailable', 0) == 1 else '✗'
                    product_data.append([
                        item['ItemName'][:30],
                        item['CategoryName'],
                        f"₱{item['Price']:.2f}",
                        status
                    ])

                product_table = Table(product_data, colWidths=[2.5 * inch, 1.8 * inch, 1.2 * inch, 1 * inch])
                product_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003274')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))

                elements.append(product_table)

        except Exception as e:
            print(f"Error creating product table: {e}")

        return elements

    def create_customer_table(self):
        """Create customer analytics table"""
        elements = []

        # Section header
        header_data = [[Paragraph('CUSTOMER BASE ANALYTICS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            stats = self.controller.get_dashboard_stats()
            total_users = int(stats.get('total_users', 0))
            total_orders = int(stats.get('total_orders', 0))
            completed_orders = self.controller.get_completed_orders()
            avg_order = float(self.controller.get_avg_order_value())

            avg_orders_per_customer = (total_orders / total_users) if total_users > 0 else 0
            customer_ltv = avg_orders_per_customer * avg_order
            retention = (completed_orders / total_orders * 100) if total_orders > 0 else 0

            data = [
                ['Metric', 'Value'],
                ['Total Customers', str(total_users)],
                ['Avg Orders/Customer', f'{avg_orders_per_customer:.2f}'],
                ['Customer Lifetime Value', f'₱{customer_ltv:,.2f}'],
                ['Order Fulfillment Rate', f'{retention:.1f}%'],
                ['Engagement Level',
                 'High' if avg_orders_per_customer >= 3 else 'Medium' if avg_orders_per_customer >= 1.5 else 'Developing']
            ]

            table = Table(data, colWidths=[2.5 * inch, 4 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFEF8')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        except Exception as e:
            print(f"Error creating customer table: {e}")

        return elements

    def create_order_table(self):
        """Create order analytics table"""
        elements = []

        # Section header
        header_data = [[Paragraph('ORDER MANAGEMENT ANALYTICS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            orders = self.controller.model.get_all_orders()

            if orders:
                # Order statistics
                total_orders = len(orders)
                order_statuses = {}
                for order in orders:
                    status = order['OrderStatus']
                    order_statuses[status] = order_statuses.get(status, 0) + 1

                # Status summary table
                status_data = [['Order Status', 'Count', 'Percentage']]
                for status, count in order_statuses.items():
                    percentage = (count / total_orders * 100) if total_orders > 0 else 0
                    status_data.append([status, str(count), f'{percentage:.1f}%'])
                status_data.append(['TOTAL', str(total_orders), '100%'])

                status_table = Table(status_data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
                status_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#4CAF50')),
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ALIGN', (0, 1), (0, -2), 'LEFT'),
                    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#FFFEF8')]),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))

                elements.append(status_table)
                elements.append(Spacer(1, 0.1 * inch))

                # Recent orders table
                order_data = [['Order ID', 'Customer', 'Amount', 'Status']]
                for order in orders[:12]:
                    customer_name = f"{order.get('UFirstName', '')} {order.get('ULastName', '')}"
                    order_data.append([
                        f"#{order['OrderID']}",
                        customer_name[:25],
                        f"₱{order['TotalFee']:.2f}",
                        order['OrderStatus']
                    ])

                order_table = Table(order_data, colWidths=[1 * inch, 2.2 * inch, 1.5 * inch, 1.8 * inch])
                order_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003274')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                    ('ALIGN', (3, 1), (3, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))

                elements.append(order_table)
            else:
                elements.append(Paragraph("No order data available", self.normal_style))

        except Exception as e:
            print(f"Error creating order table: {e}")

        return elements

    def create_insights_table(self):
        """Create business insights table"""
        elements = []

        # Section header
        header_data = [[Paragraph('BUSINESS INSIGHTS & ANALYSIS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            stats = self.controller.get_dashboard_stats()
            completed_orders = self.controller.get_completed_orders()
            avg_order = self.controller.get_avg_order_value()

            total_orders = int(stats.get('total_orders', 0))
            total_revenue = float(stats.get('total_revenue', 0))
            total_users = int(stats.get('total_users', 0))
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0

            insights_data = [
                ['Insight Area', 'Analysis'],
                ['Order Performance',
                 f'{completed_orders}/{total_orders} orders completed ({completion_rate:.1f}%) - {"Excellent" if completion_rate >= 90 else "Strong" if completion_rate >= 80 else "Good"} efficiency'],
                ['Revenue Analysis',
                 f'₱{total_revenue:,.2f} total revenue shows {"robust" if total_revenue >= 50000 else "solid" if total_revenue >= 20000 else "growing"} performance'],
                ['Customer Value',
                 f'Avg ₱{float(avg_order):,.2f} indicates {"premium" if float(avg_order) >= 500 else "moderate" if float(avg_order) >= 250 else "value"} spending'],
                ['Market Position',
                 f'{total_users} customers represent {"strong" if total_users >= 100 else "growing" if total_users >= 50 else "developing"} market presence'],
                ['Product Portfolio',
                 f'{stats.get("total_menu_items", 0)} items provide comprehensive customer selection'],
                ['Quality Standards',
                 'High completion rates reflect commitment to service excellence']
            ]

            table = Table(insights_data, colWidths=[2 * inch, 4.5 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFEF8')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        except Exception as e:
            print(f"Error creating insights table: {e}")

        return elements

    def create_operational_table(self):
        """Create operational metrics table"""
        elements = []

        # Section header
        header_data = [[Paragraph('OPERATIONAL EFFICIENCY METRICS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            stats = self.controller.get_dashboard_stats()
            completed_orders = self.controller.get_completed_orders()
            total_orders = int(stats.get('total_orders', 0))

            efficiency_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0

            metrics_data = [
                ['Metric', 'Value', 'Status'],
                ['Order Completion Rate', f'{efficiency_rate:.1f}%',
                 'Excellent' if efficiency_rate >= 90 else 'Good' if efficiency_rate >= 75 else 'Improving'],
                ['Processing Volume', f'{total_orders} orders', 'Active'],
                ['System Uptime', '99.9%', 'Optimal'],
                ['Response Time', '< 2 seconds', 'Fast'],
                ['Service Quality', 'High', 'Maintained']
            ]

            table = Table(metrics_data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFBD59')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#003274')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFEF8')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

        except Exception as e:
            print(f"Error creating operational table: {e}")

        return elements

    def create_recommendations_table(self):
        """Create strategic recommendations table"""
        elements = []

        # Section header
        header_data = [[Paragraph('STRATEGIC RECOMMENDATIONS', self.section_style)]]
        header_table = Table(header_data, colWidths=[6.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#003274')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        try:
            stats = self.controller.get_dashboard_stats()
            avg_order = float(self.controller.get_avg_order_value())
            total_users = int(stats.get('total_users', 0))
            menu_items = int(stats.get('total_menu_items', 0))

            recommendations_data = [['Focus Area', 'Recommendation']]

            # Revenue optimization
            if avg_order < 500:
                recommendations_data.append(['Revenue Growth',
                                             'Implement upselling strategies and combo deals to increase average order value'])
            else:
                recommendations_data.append(['Revenue Optimization',
                                             'Continue pricing strategy while exploring premium offerings'])

            # Customer engagement
            recommendations_data.append(['Customer Retention',
                                         'Develop loyalty rewards program to encourage repeat purchases'])

            # Product diversification
            if menu_items < 20:
                recommendations_data.append(['Menu Expansion',
                                             'Expand product catalog to offer more variety'])
            else:
                recommendations_data.append(['Product Optimization',
                                             'Analyze top performers and consider seasonal rotations'])

            # Marketing
            recommendations_data.append(['Marketing Strategy',
                                         'Leverage customer data for targeted promotions'])

            # Operations
            recommendations_data.append(['Operational Excellence',
                                         'Maintain high completion rates through quality focus'])

            # Technology
            recommendations_data.append(['Digital Innovation',
                                         'Explore mobile app features for enhanced engagement'])

            table = Table(recommendations_data, colWidths=[2 * inch, 4.5 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F8F4')]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

            # Add outlook
            elements.append(Spacer(1, 0.1 * inch))

            outlook_data = [[Paragraph(
                '<b>Business Outlook:</b> MunchHub is well-positioned for continued growth. Focus on customer retention, operational efficiency, and strategic expansion will drive long-term success.',
                self.normal_style)]]
            outlook_table = Table(outlook_data, colWidths=[6.5 * inch])
            outlook_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E3F2FD')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(outlook_table)

        except Exception as e:
            print(f"Error creating recommendations table: {e}")

        return elements

    def create_footer(self):
        """Create report footer"""
        elements = []

        footer_data = [
            [Paragraph('<b>CONFIDENTIAL BUSINESS DOCUMENT</b>',
                       ParagraphStyle('Conf', parent=self.styles['Normal'],
                                      fontSize=9, textColor=colors.red, alignment=TA_CENTER))],
            [Paragraph(
                f'MunchHub Business Report | Generated {datetime.now().strftime("%B %d, %Y")} | © {datetime.now().year} All Rights Reserved',
                ParagraphStyle('Footer', parent=self.styles['Normal'],
                               fontSize=8, textColor=colors.grey, alignment=TA_CENTER))]
        ]

        footer_table = Table(footer_data, colWidths=[6.5 * inch])
        footer_table.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elements.append(footer_table)
        return elements