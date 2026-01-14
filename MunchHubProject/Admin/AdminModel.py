class AdminModel:
    """Model for Admin Dashboard - handles database operations"""

    def __init__(self, db_manager):
        self.db = db_manager

    # Dashboard Statistics
    def get_total_users(self):
        """Get total number of users"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Users")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting total users: {e}")
            return 0

    def get_total_orders(self):
        """Get total number of orders"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Orders")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting total orders: {e}")
            return 0

    def get_total_revenue(self):
        """Get total revenue"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT SUM(TotalFee) FROM Orders WHERE OrderStatus = 'Delivered'")
            result = cursor.fetchone()
            cursor.close()
            return f"{result[0]:.2f}" if result and result[0] else "0.00"
        except Exception as e:
            print(f"Error getting total revenue: {e}")
            return "0.00"

    def get_total_menu_items(self):
        """Get total menu items"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM MenuItems")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting total menu items: {e}")
            return 0

    def get_monthly_sales_data(self):
        """Get sales data grouped by month"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            # Get current year sales
            query = """
                SELECT 
                    MONTH(CURRENT_DATE) as month,
                    COALESCE(SUM(TotalFee), 0) as total
                FROM Orders
                WHERE OrderStatus = 'Delivered'
                AND YEAR(CURRENT_DATE) = YEAR(CURRENT_DATE)
                GROUP BY MONTH(CURRENT_DATE)
                ORDER BY month
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Create data for all 12 months
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            sales_data = {month: 0 for month in months}

            for row in results:
                month_name = months[row['month'] - 1]
                sales_data[month_name] = float(row['total'])

            return sales_data
        except Exception as e:
            print(f"Error getting monthly sales: {e}")
            return {month: 0 for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}

    # Activity Logs
    def get_activity_logs(self, limit=100):
        """Get activity logs"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            # You'll need to create an activity_logs table
            # For now, we'll simulate with user/staff activities
            query = """
                SELECT 
                    u.Username as user,
                    'Login' as action,
                    NOW() as timestamp,
                    CASE 
                        WHEN s.StaffID IS NOT NULL THEN 'Staff'
                        WHEN c.CustomerID IS NOT NULL THEN 'Customer'
                        ELSE 'User'
                    END as user_type
                FROM Users u
                LEFT JOIN Staffs s ON u.UserID = s.UserID
                LEFT JOIN Customers c ON u.UserID = c.UserID
                ORDER BY u.UserID DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting activity logs: {e}")
            return []

    def filter_activity_logs(self, search_text, start_date=None, end_date=None):
        """Filter activity logs"""
        # Implement filtering logic
        return self.get_activity_logs()

    # Menu Items
    def get_all_menu_items(self):
        """Get all menu items"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.MenuID, m.ItemName, c.CategoryName, m.Price, m.isAvailable, m.CategoryID
                FROM menuitems m
                JOIN categories c ON m.CategoryID = c.CategoryID
                ORDER BY m.MenuID
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting menu items: {e}")
            return []

    def get_menu_item(self, menu_id):
        """Get single menu item"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT MenuID, ItemName, CategoryID, Price, isAvailable
                FROM menuitems
                WHERE MenuID = %s
            """, (menu_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting menu item: {e}")
            return None

    def add_menu_item(self, menu_id, category_id, item_name, price, is_available):
        """Add new menu item"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT MenuID FROM menuitems WHERE MenuID = %s", (menu_id,))
            if cursor.fetchone():
                cursor.close()
                return False, f"Menu ID '{menu_id}' already exists"

            query = """
                INSERT INTO menuitems (MenuID, CategoryID, ItemName, Price, isAvailable)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (menu_id, category_id, item_name, float(price), is_available))
            self.db.connection.commit()
            cursor.close()
            return True, "Menu item added successfully"
        except Exception as e:
            print(f"Error adding menu item: {e}")
            return False, str(e)

    def update_menu_item(self, menu_id, category_id, item_name, price, is_available):
        """Update menu item"""
        try:
            cursor = self.db.connection.cursor()
            query = """
                UPDATE menuitems
                SET ItemName = %s, CategoryID = %s, Price = %s, isAvailable = %s
                WHERE MenuID = %s
            """
            cursor.execute(query, (item_name, category_id, float(price), is_available, menu_id))
            self.db.connection.commit()
            cursor.close()
            return True, "Menu item updated successfully"
        except Exception as e:
            print(f"Error updating menu item: {e}")
            return False, str(e)

    def delete_menu_item(self, menu_id):
        """Delete menu item"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM menuitems WHERE MenuID = %s", (menu_id,))
            self.db.connection.commit()
            cursor.close()
            return True, "Menu item deleted successfully"
        except Exception as e:
            print(f"Error deleting menu item: {e}")
            return False, str(e)

    # Categories
    def get_all_categories(self):
        """Get all categories"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT CategoryID, CategoryName, Description
                FROM categories
                ORDER BY CategoryID
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    def get_category(self, category_id):
        """Get single category"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT CategoryID, CategoryName, Description
                FROM categories
                WHERE CategoryID = %s
            """, (category_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting category: {e}")
            return None

    def add_category(self, category_id, category_name, description):
        """Add new category"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT CategoryID FROM categories WHERE CategoryID = %s", (category_id,))
            if cursor.fetchone():
                cursor.close()
                return False, f"Category ID '{category_id}' already exists"

            query = """
                INSERT INTO categories (CategoryID, CategoryName, Description)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (category_id, category_name, description))
            self.db.connection.commit()
            cursor.close()
            return True, "Category added successfully"
        except Exception as e:
            print(f"Error adding category: {e}")
            return False, str(e)

    def update_category(self, category_id, category_name, description):
        """Update category"""
        try:
            cursor = self.db.connection.cursor()
            query = """
                UPDATE categories
                SET CategoryName = %s, Description = %s
                WHERE CategoryID = %s
            """
            cursor.execute(query, (category_name, description, category_id))
            self.db.connection.commit()
            cursor.close()
            return True, "Category updated successfully"
        except Exception as e:
            print(f"Error updating category: {e}")
            return False, str(e)

    def delete_category(self, category_id):
        """Delete category"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM categories WHERE CategoryID = %s", (category_id,))
            self.db.connection.commit()
            cursor.close()
            return True, "Category deleted successfully"
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False, str(e)

    # Orders
    def get_all_orders(self):
        """Get all orders"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT o.OrderID, u.UFirstName, u.ULastName, o.TotalFee, 
                       o.DeliveryFee, o.OrderStatus, NOW() as OrderDate
                FROM Orders o
                JOIN Customers c ON o.CustomerID = c.CustomerID
                JOIN Users u ON c.UserID = u.UserID
                ORDER BY o.OrderID DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []

    def update_order_status(self, order_id, new_status):
        """Update order status"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("UPDATE Orders SET OrderStatus = %s WHERE OrderID = %s",
                           (new_status, order_id))
            self.db.connection.commit()
            cursor.close()
            return True, f"Order status updated to '{new_status}'"
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False, str(e)

    def get_order_details(self, order_id):
        """Get order details"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT o.*, u.UFirstName, u.ULastName, u.PhoneNum
                FROM Orders o
                JOIN Customers c ON o.CustomerID = c.CustomerID
                JOIN Users u ON c.UserID = u.UserID
                WHERE o.OrderID = %s
            """
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting order details: {e}")
            return None

    # Staff
    def get_all_staff(self):
        """Get all staff members"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT s.StaffID, u.UFirstName, u.UMiddleName, u.ULastName, 
                       u.Username, u.PhoneNum
                FROM Staffs s
                JOIN Users u ON s.UserID = u.UserID
                ORDER BY s.StaffID
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting staff: {e}")
            return []

    def delete_staff(self, staff_id):
        """Delete staff member"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM Staffs WHERE StaffID = %s", (staff_id,))
            self.db.connection.commit()
            cursor.close()
            return True, "Staff member removed successfully"
        except Exception as e:
            print(f"Error deleting staff: {e}")
            return False, str(e)

    # Reports
    def get_completed_orders(self):
        """Get completed orders count"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Orders WHERE OrderStatus = 'Delivered'")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting completed orders: {e}")
            return 0

    def get_avg_order_value(self):
        """Get average order value"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT AVG(TotalFee) FROM Orders WHERE OrderStatus = 'Delivered'")
            result = cursor.fetchone()
            cursor.close()
            return f"{result[0]:.2f}" if result and result[0] else "0.00"
        except Exception as e:
            print(f"Error getting avg order value: {e}")
            return "0.00"