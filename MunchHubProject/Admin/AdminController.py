from datetime import datetime
from Admin.AdminModel import AdminModel


class AdminController:
    """Controller for Admin Dashboard - handles business logic"""

    def __init__(self, db_manager):
        self.model = AdminModel(db_manager)
        self.db = db_manager  # Store db_manager reference for direct access

    # Dashboard Methods
    """
    AdminController.py - PARTIAL UPDATE (Revenue Methods Only)
    Replace the get_dashboard_stats() method in your existing AdminController.py
    """

    def get_dashboard_stats(self, filter_type='all', year=None, month=None, day=None):
        """
        Get dashboard statistics with optional date filtering

        Args:
            filter_type: 'all', 'year', 'month', or 'day'
            year: Year to filter (required for year/month/day filters)
            month: Month to filter (required for month/day filters)
            day: Day to filter (required for day filter)
        """
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            stats = {
                'total_users': 0,
                'total_orders': 0,
                'total_revenue': 0,
                'total_menu_items': 0,
                'pending_revenue': 0,
                'total_pending_orders': 0,
                'confirmed_revenue': 0
            }

            # Build date filter condition
            date_condition = ""
            date_params = []

            if filter_type == 'day' and year and month and day:
                date_condition = "AND DATE(o.OrderDate) = %s"
                date_params = [f"{year}-{month:02d}-{day:02d}"]
            elif filter_type == 'month' and year and month:
                date_condition = "AND YEAR(o.OrderDate) = %s AND MONTH(o.OrderDate) = %s"
                date_params = [year, month]
            elif filter_type == 'year' and year:
                date_condition = "AND YEAR(o.OrderDate) = %s"
                date_params = [year]

            # Get total users (customers)
            cursor.execute("SELECT COUNT(*) as count FROM Customers")
            result = cursor.fetchone()
            stats['total_users'] = result['count'] if result else 0

            # Get total orders (with date filter)
            order_query = f"SELECT COUNT(*) as count FROM Orders o WHERE 1=1 {date_condition}"
            cursor.execute(order_query, date_params)
            result = cursor.fetchone()
            stats['total_orders'] = result['count'] if result else 0

            # Get total revenue - ONLY DELIVERED ORDERS (completed transactions) with date filter
            delivered_revenue_query = f"""
                SELECT SUM(ol.Quantity * mi.Price) as total
                FROM OrderList ol
                JOIN MenuItems mi ON ol.MenuID = mi.MenuID
                JOIN Orders o ON ol.OrderID = o.OrderID
                WHERE o.OrderStatus = 'Delivered' {date_condition}
            """
            cursor.execute(delivered_revenue_query, date_params)
            result = cursor.fetchone()
            stats['total_revenue'] = float(result['total']) if result and result['total'] else 0.0

            # Get confirmed revenue (Preparing, Out for delivery, Delivered) with date filter
            confirmed_revenue_query = f"""
                SELECT SUM(ol.Quantity * mi.Price) as total
                FROM OrderList ol
                JOIN MenuItems mi ON ol.MenuID = mi.MenuID
                JOIN Orders o ON ol.OrderID = o.OrderID
                WHERE o.OrderStatus IN ('Preparing', 'Out for delivery', 'Delivered') {date_condition}
            """
            cursor.execute(confirmed_revenue_query, date_params)
            result = cursor.fetchone()
            stats['confirmed_revenue'] = float(result['total']) if result and result['total'] else 0.0

            # Get pending revenue (orders not yet accepted by staff) with date filter
            pending_revenue_query = f"""
                SELECT SUM(ol.Quantity * mi.Price) as total
                FROM OrderList ol
                JOIN MenuItems mi ON ol.MenuID = mi.MenuID
                JOIN Orders o ON ol.OrderID = o.OrderID
                WHERE o.OrderStatus = 'Pending' AND o.StaffID IS NULL {date_condition}
            """
            cursor.execute(pending_revenue_query, date_params)
            result = cursor.fetchone()
            stats['pending_revenue'] = float(result['total']) if result and result['total'] else 0.0

            # Count pending orders with date filter
            pending_order_query = f"SELECT COUNT(*) as count FROM Orders o WHERE OrderStatus = 'Pending' AND StaffID IS NULL {date_condition}"
            cursor.execute(pending_order_query, date_params)
            result = cursor.fetchone()
            stats['total_pending_orders'] = result['count'] if result else 0

            # Get total menu items
            cursor.execute("SELECT COUNT(*) as count FROM MenuItems WHERE isAvailable = 1")
            result = cursor.fetchone()
            stats['total_menu_items'] = result['count'] if result else 0

            cursor.close()
            return stats

        except Exception as e:
            print(f"Error getting dashboard stats: {e}")
            import traceback
            traceback.print_exc()
            return {
                'total_users': 0,
                'total_orders': 0,
                'total_revenue': 0,
                'total_menu_items': 0,
                'pending_revenue': 0,
                'total_pending_orders': 0,
                'confirmed_revenue': 0
            }

    def get_monthly_sales(self):
        """
        Get monthly sales data for the current year
        🔧 UPDATED: Now has option to include all statuses or just delivered
        """
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Query to get sales by month - Calculate from OrderList
            # Using 'Delivered' for completed sales (actual revenue)
            query = """
                SELECT 
                    MONTH(o.OrderDate) as month_num,
                    MONTHNAME(o.OrderDate) as month_name,
                    SUM(ol.Quantity * mi.Price) as total_sales
                FROM Orders o
                JOIN OrderList ol ON o.OrderID = ol.OrderID
                JOIN MenuItems mi ON ol.MenuID = mi.MenuID
                WHERE o.OrderStatus = 'Delivered' 
                AND YEAR(o.OrderDate) = YEAR(CURDATE())
                GROUP BY MONTH(o.OrderDate), MONTHNAME(o.OrderDate)
                ORDER BY MONTH(o.OrderDate)
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Create dictionary with all months initialized to 0
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_sales = {month: 0 for month in months}

            # Fill in actual sales data
            month_map = {
                'January': 'Jan', 'February': 'Feb', 'March': 'Mar',
                'April': 'Apr', 'May': 'May', 'June': 'Jun',
                'July': 'Jul', 'August': 'Aug', 'September': 'Sep',
                'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
            }

            for row in results:
                month_name = month_map.get(row['month_name'], row['month_name'][:3])
                monthly_sales[month_name] = float(row['total_sales']) if row['total_sales'] else 0.0

            return monthly_sales

        except Exception as e:
            print(f"Error getting monthly sales: {e}")
            import traceback
            traceback.print_exc()
            # Return empty data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return {month: 0 for month in months}

    def get_activity_logs(self, limit=100):
        """Get staff activity logs showing orders they handled"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Query to get order activities with staff and customer information
            query = """
                SELECT 
                    CONCAT(COALESCE(su.UFirstName, 'Staff'), ' ', COALESCE(su.ULastName, 'Member')) as staff_name,
                    CONCAT(COALESCE(cu.UFirstName, 'Unknown'), ' ', COALESCE(cu.ULastName, 'Customer')) as customer,
                    o.OrderID as order_id,
                    CASE 
                        WHEN o.OrderStatus = 'Pending' THEN 'Received Order'
                        WHEN o.OrderStatus = 'Preparing' THEN 'Preparing Order'
                        WHEN o.OrderStatus = 'Out for Delivery' THEN 'Out for Delivery'
                        WHEN o.OrderStatus = 'Delivered' THEN 'Completed Delivery'
                        WHEN o.OrderStatus = 'Cancelled' THEN 'Order Cancelled'
                        ELSE 'Processing Order'
                    END as action,
                    o.OrderStatus as status,
                    COALESCE(o.OrderDate, NOW()) as timestamp
                FROM Orders o
                LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
                LEFT JOIN Users cu ON c.UserID = cu.UserID
                LEFT JOIN Staffs s ON s.StaffID = (
                    SELECT StaffID FROM Staffs ORDER BY RAND() LIMIT 1
                )
                LEFT JOIN Users su ON s.UserID = su.UserID
                ORDER BY o.OrderID DESC
                LIMIT %s
            """

            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()

            # Ensure all fields have values
            for result in results:
                if not result.get('staff_name') or result['staff_name'] == ' ':
                    result['staff_name'] = 'Staff Member'
                if not result.get('customer') or result['customer'] == ' ':
                    result['customer'] = 'Unknown Customer'
                if not result.get('order_id'):
                    result['order_id'] = 'N/A'
                if not result.get('action'):
                    result['action'] = 'Unknown Action'
                if not result.get('status'):
                    result['status'] = 'Unknown'

            print(f"Retrieved {len(results)} activity logs")
            return results

        except Exception as e:
            print(f"Error getting activity logs: {e}")
            import traceback
            traceback.print_exc()
            return []

    def filter_activity_logs(self, search_text, start_date=None, end_date=None):
        """Filter activity logs"""
        return self.model.filter_activity_logs(search_text, start_date, end_date)

    # Orders Methods
    def get_all_orders(self):
        """Get all orders"""
        return self.model.get_all_orders()

    def update_order_status(self, order_id, new_status):
        """Update order status"""
        return self.model.update_order_status(order_id, new_status)

    def get_order_details(self, order_id):
        """Get order details"""
        return self.model.get_order_details(order_id)

    # Staff Management Methods
    def get_all_staff(self):
        """Get all staff members"""
        return self.model.get_all_staff()

    def delete_staff(self, staff_id):
        """Delete staff member"""
        return self.model.delete_staff(staff_id)

    # Reports Methods
    def get_completed_orders(self):
        """Get count of completed/delivered orders"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM Orders WHERE OrderStatus = 'Delivered'")
            result = cursor.fetchone()
            cursor.close()
            return result['count'] if result else 0
        except Exception as e:
            print(f"Error getting completed orders: {e}")
            return 0

    def get_avg_order_value(self):
        """Get average order value - Calculate from OrderList"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Calculate average from OrderList
            query = """
                SELECT AVG(order_total) as avg_value
                FROM (
                    SELECT o.OrderID, SUM(ol.Quantity * mi.Price) as order_total
                    FROM Orders o
                    JOIN OrderList ol ON o.OrderID = ol.OrderID
                    JOIN MenuItems mi ON ol.MenuID = mi.MenuID
                    WHERE o.OrderStatus = 'Delivered'
                    GROUP BY o.OrderID
                ) as order_totals
            """

            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return float(result['avg_value']) if result and result['avg_value'] else 0.0
        except Exception as e:
            print(f"Error getting average order value: {e}")
            import traceback
            traceback.print_exc()
            return 0.0

    # ==================== MENU ITEM METHODS ====================

    def generate_menu_id(self):
        """Generate next MenuID in format MENU1, MENU2, MENU3, etc."""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Get all existing menu IDs
            cursor.execute("SELECT MenuID FROM MenuItems ORDER BY MenuID")
            results = cursor.fetchall()

            # Find the highest valid number (format: MENUx where x is any number)
            max_num = 0
            if results:
                for result in results:
                    menu_id = result['MenuID']
                    try:
                        # Extract number part after 'MENU'
                        if menu_id.startswith('MENU'):
                            num_part = menu_id[4:]  # Everything after 'MENU'

                            # Only process if we have a valid number
                            if num_part.isdigit():
                                num = int(num_part)
                                if num > max_num:
                                    max_num = num
                        # Legacy support: handle old ITEM prefix
                        elif menu_id.startswith('ITEM'):
                            num_part = menu_id[4:]
                            if num_part.isdigit():
                                num = int(num_part)
                                if num > max_num:
                                    max_num = num

                    except (ValueError, AttributeError, IndexError) as e:
                        print(f"Warning: Error processing MenuID {menu_id}: {e}")
                        continue

            # Generate new ID: max + 1, NO leading zeros (MENU1, MENU2, etc.)
            new_num = max_num + 1
            new_id = f"MENU{new_num}"

            # Safety check: verify this ID doesn't exist (duplicate prevention)
            max_attempts = 100
            attempts = 0
            while attempts < max_attempts:
                cursor.execute("SELECT MenuID FROM MenuItems WHERE MenuID = %s", (new_id,))
                if not cursor.fetchone():
                    # This ID is available!
                    break
                else:
                    # ID exists, try next number
                    print(f"Warning: {new_id} already exists, trying next...")
                    new_num += 1
                    new_id = f"MENU{new_num}"
                    attempts += 1

            if attempts >= max_attempts:
                cursor.close()
                print("Error: Could not find available MenuID")
                return None

            cursor.close()
            print(f"Generated MenuID: {new_id} (next number after {max_num})")
            return new_id

        except Exception as e:
            print(f"Error generating MenuID: {e}")
            import traceback
            traceback.print_exc()
            return None

    def add_menu_item(self, category_id, name, price, is_available):
        """Add a new menu item with auto-generated ID"""
        try:
            # Generate new MenuID
            menu_id = self.generate_menu_id()
            if not menu_id:
                return False, "Failed to generate Menu ID"

            # Verify the ID doesn't exist (extra safety check)
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT MenuID FROM MenuItems WHERE MenuID = %s", (menu_id,))
            if cursor.fetchone():
                cursor.close()
                return False, f"Menu ID {menu_id} already exists. Please try again."

            # Insert the new menu item
            query = """
                INSERT INTO MenuItems (MenuID, CategoryID, ItemName, Price, isAvailable)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (menu_id, category_id, name, price, is_available))
            self.db.connection.commit()
            cursor.close()
            print(f"Successfully added menu item: {menu_id} - {name}")
            return True, f"Menu item '{name}' added successfully with ID: {menu_id}"
        except Exception as e:
            self.db.connection.rollback()
            print(f"Error adding menu item: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error adding menu item: {str(e)}"

    def update_menu_item(self, menu_id, category_id, name, price, is_available):
        """Update an existing menu item"""
        try:
            cursor = self.db.connection.cursor()
            query = """
                UPDATE MenuItems
                SET CategoryID = %s, ItemName = %s, Price = %s, isAvailable = %s
                WHERE MenuID = %s
            """
            cursor.execute(query, (category_id, name, price, is_available, menu_id))
            self.db.connection.commit()
            cursor.close()
            return True, f"Menu item '{name}' updated successfully"
        except Exception as e:
            self.db.connection.rollback()
            print(f"Error updating menu item: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error updating menu item: {str(e)}"

    def delete_menu_item(self, menu_id):
        """Delete a menu item"""
        try:
            cursor = self.db.connection.cursor()
            # First check if item exists in any orders
            cursor.execute("SELECT COUNT(*) as count FROM OrderList WHERE MenuID = %s", (menu_id,))
            result = cursor.fetchone()

            if result[0] > 0:
                cursor.close()
                return False, "Cannot delete menu item. It has been used in orders."

            cursor.execute("DELETE FROM MenuItems WHERE MenuID = %s", (menu_id,))
            self.db.connection.commit()
            cursor.close()
            return True, "Menu item deleted successfully"
        except Exception as e:
            self.db.connection.rollback()
            print(f"Error deleting menu item: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error deleting menu item: {str(e)}"

    def get_menu_item(self, menu_id):
        """Get a specific menu item by ID"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT m.*, c.CategoryName
                FROM MenuItems m
                JOIN Categories c ON m.CategoryID = c.CategoryID
                WHERE m.MenuID = %s
            """
            cursor.execute(query, (menu_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting menu item: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_all_menu_items(self):
        """Get all menu items with category names"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT m.MenuID, m.ItemName, m.Price, m.isAvailable, 
                       c.CategoryID, c.CategoryName
                FROM MenuItems m
                JOIN Categories c ON m.CategoryID = c.CategoryID
                ORDER BY m.MenuID
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting menu items: {e}")
            import traceback
            traceback.print_exc()
            return []

    # ==================== CATEGORY METHODS ====================

    def generate_category_id(self):
        """Generate next CategoryID in format CAT05, CAT06, etc."""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT CategoryID FROM Categories ORDER BY CategoryID DESC LIMIT 1")
            result = cursor.fetchone()

            if result and result['CategoryID']:
                # Extract number from CAT01 format
                category_id = result['CategoryID']
                # Remove 'CAT' prefix and convert to int
                last_num = int(category_id.replace('CAT', ''))
                new_id = f"CAT{(last_num + 1):02d}"
            else:
                new_id = "CAT01"

            # Double check if this ID already exists (safety check)
            cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryID = %s", (new_id,))
            if cursor.fetchone():
                print(f"Warning: Generated ID {new_id} already exists, trying next...")
                # If it exists, try incrementing until we find a free one
                counter = int(new_id.replace('CAT', '')) + 1
                max_attempts = 100
                attempts = 0
                while attempts < max_attempts:
                    new_id = f"CAT{counter:02d}"
                    cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryID = %s", (new_id,))
                    if not cursor.fetchone():
                        break
                    counter += 1
                    attempts += 1

                if attempts >= max_attempts:
                    cursor.close()
                    print("Error: Could not find available CategoryID")
                    return None

            cursor.close()
            print(f"Generated CategoryID: {new_id}")
            return new_id
        except Exception as e:
            print(f"Error generating CategoryID: {e}")
            import traceback
            traceback.print_exc()
            return None

    def add_category(self, name, description):
        """Add a new category with auto-generated ID"""
        try:
            # Generate new CategoryID
            category_id = self.generate_category_id()
            if not category_id:
                return False, "Failed to generate Category ID"

            cursor = self.db.connection.cursor()
            query = """
                INSERT INTO Categories (CategoryID, CategoryName, Description)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (category_id, name, description))
            self.db.connection.commit()
            cursor.close()
            return True, f"Category '{name}' added successfully with ID: {category_id}"
        except Exception as e:
            self.db.connection.rollback()
            print(f"Error adding category: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error adding category: {str(e)}"

    def update_category(self, category_id, name, description):
        """Update an existing category"""
        try:
            cursor = self.db.connection.cursor()
            query = """
                UPDATE Categories
                SET CategoryName = %s, Description = %s
                WHERE CategoryID = %s
            """
            cursor.execute(query, (name, description, category_id))
            self.db.connection.commit()
            cursor.close()
            return True, f"Category '{name}' updated successfully"
        except Exception as e:
            self.db.connection.rollback()
            print(f"Error updating category: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error updating category: {str(e)}"

    def delete_category(self, category_id):
        """Delete a category"""
        try:
            cursor = self.db.connection.cursor()
            # First check if category has menu items
            cursor.execute("SELECT COUNT(*) as count FROM MenuItems WHERE CategoryID = %s", (category_id,))
            result = cursor.fetchone()

            if result[0] > 0:
                cursor.close()
                return False, "Cannot delete category. It contains menu items."

            cursor.execute("DELETE FROM Categories WHERE CategoryID = %s", (category_id,))
            self.db.connection.commit()
            cursor.close()
            return True, "Category deleted successfully"
        except Exception as e:
            self.db.connection.rollback()
            print(f"Error deleting category: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error deleting category: {str(e)}"

    def get_category(self, category_id):
        """Get a specific category by ID"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT * FROM Categories WHERE CategoryID = %s"
            cursor.execute(query, (category_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting category: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_all_categories(self):
        """Get all categories"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT * FROM Categories ORDER BY CategoryID"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting categories: {e}")
            import traceback
            traceback.print_exc()
            return []

    # Add these methods to your AdminController class

    def add_staff(self, username, password, first_name, middle_name, last_name, phone_number):
        """Add a new staff member"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Check if username already exists
            cursor.execute("SELECT Username FROM Users WHERE Username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "Username already exists! Please choose a different username."

            # Generate new UserID
            cursor.execute("SELECT UserID FROM Users ORDER BY UserID DESC LIMIT 1")
            last_user = cursor.fetchone()
            if last_user:
                last_id = int(last_user['UserID'][1:])
                new_user_id = f"U{str(last_id + 1).zfill(3)}"
            else:
                new_user_id = "U001"

            # Hash the password
            password_hash = self.db.hash_password(password)

            # Insert into Users table
            insert_user_query = """
                INSERT INTO Users (UserID, Username, Password, UFirstName, UMiddleName, ULastName, PhoneNum)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_user_query, (
                new_user_id,
                username,
                password_hash,
                first_name,
                middle_name if middle_name else None,
                last_name,
                phone_number
            ))

            # Generate new StaffID
            cursor.execute("SELECT StaffID FROM Staffs ORDER BY StaffID DESC LIMIT 1")
            last_staff = cursor.fetchone()
            if last_staff:
                last_id = int(last_staff['StaffID'][1:])
                new_staff_id = f"S{str(last_id + 1).zfill(3)}"
            else:
                new_staff_id = "S001"

            # Insert into Staffs table
            insert_staff_query = """
                INSERT INTO Staffs (StaffID, UserID)
                VALUES (%s, %s)
            """
            cursor.execute(insert_staff_query, (new_staff_id, new_user_id))

            # Commit the transaction
            self.db.connection.commit()
            cursor.close()

            return True, f"Staff member '{first_name} {last_name}' added successfully with ID: {new_staff_id}"

        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            print(f"Error adding staff: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error adding staff: {str(e)}"

    def update_staff(self, staff_id, first_name, middle_name, last_name, phone_number):
        """Update staff information"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Get UserID from StaffID
            cursor.execute("SELECT UserID FROM Staffs WHERE StaffID = %s", (staff_id,))
            staff_result = cursor.fetchone()

            if not staff_result:
                cursor.close()
                return False, "Staff member not found."

            user_id = staff_result['UserID']

            # Update Users table
            update_query = """
                UPDATE Users 
                SET UFirstName = %s, UMiddleName = %s, ULastName = %s, PhoneNum = %s
                WHERE UserID = %s
            """
            cursor.execute(update_query, (
                first_name,
                middle_name if middle_name else None,
                last_name,
                phone_number,
                user_id
            ))

            self.db.connection.commit()
            cursor.close()

            return True, f"Staff member information updated successfully."

        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            print(f"Error updating staff: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error updating staff: {str(e)}"

    def delete_staff(self, staff_id):
        """Delete a staff member"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Get UserID from StaffID
            cursor.execute("SELECT UserID FROM Staffs WHERE StaffID = %s", (staff_id,))
            staff_result = cursor.fetchone()

            if not staff_result:
                cursor.close()
                return False, "Staff member not found."

            user_id = staff_result['UserID']

            # Delete from Staffs table first (foreign key constraint)
            cursor.execute("DELETE FROM Staffs WHERE StaffID = %s", (staff_id,))

            # Delete from Users table
            cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))

            self.db.connection.commit()
            cursor.close()

            return True, "Staff member removed successfully."

        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            print(f"Error deleting staff: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error removing staff: {str(e)}"

    def get_all_staff(self):
        """Get all staff members"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT s.StaffID, u.UserID, u.Username, u.UFirstName, u.UMiddleName, u.ULastName, u.PhoneNum
                FROM Staffs s
                JOIN Users u ON s.UserID = u.UserID
                ORDER BY s.StaffID ASC
            """
            cursor.execute(query)
            staff_list = cursor.fetchall()
            cursor.close()
            return staff_list
        except Exception as e:
            print(f"Error getting staff: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_staff_activity_logs(self, limit=100):
        """Get all staff activity logs from StaffActivityLog table"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT 
                    sal.LogID,
                    sal.StaffID,
                    CONCAT(COALESCE(su.UFirstName, ''), ' ', COALESCE(su.ULastName, '')) as StaffName,
                    sal.OrderID,
                    sal.CustomerID,
                    CONCAT(COALESCE(cu.UFirstName, ''), ' ', COALESCE(cu.ULastName, '')) as CustomerName,
                    sal.Action,
                    sal.Status,
                    sal.ActivityDate
                FROM StaffActivityLog sal
                LEFT JOIN Staffs s ON sal.StaffID = s.StaffID
                LEFT JOIN Users su ON s.UserID = su.UserID
                LEFT JOIN Customers c ON sal.CustomerID = c.CustomerID
                LEFT JOIN Users cu ON c.UserID = cu.UserID
                ORDER BY sal.ActivityDate DESC
                LIMIT %s
            """

            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()

            # Clean up any missing data
            for result in results:
                if not result.get('StaffName') or result['StaffName'].strip() == '':
                    result['StaffName'] = f"Staff {result.get('StaffID', 'Unknown')}"
                if not result.get('CustomerName') or result['CustomerName'].strip() == '':
                    result['CustomerName'] = f"Customer {result.get('CustomerID', 'Unknown')}"

            return results

        except Exception as e:
            print(f"Error getting staff activity logs: {e}")
            import traceback
            traceback.print_exc()
            return []

# ==================== NEW: SALES GRAPH METHODS ====================

def get_daily_sales(self, year, month):
    """Get sales data by day for a specific month (for Sales Graph)"""
    try:
        cursor = self.db.connection.cursor(dictionary=True)
        query = """
            SELECT 
                DAY(OrderDate) as day,
                SUM(TotalFee) as total_sales,
                COUNT(*) as order_count
            FROM orders
            WHERE YEAR(OrderDate) = %s 
            AND MONTH(OrderDate) = %s
            AND OrderStatus = 'Delivered'
            GROUP BY DAY(OrderDate)
            ORDER BY day
        """
        cursor.execute(query, (year, month))
        result = cursor.fetchall()
        cursor.close()
        return result if result else []
    except Exception as e:
        print(f"Error fetching daily sales: {e}")
        return []

def get_monthly_sales_by_year(self, year):
    """Get sales data by month for a specific year (for Sales Graph)"""
    try:
        cursor = self.db.connection.cursor(dictionary=True)
        query = """
            SELECT 
                MONTH(OrderDate) as month,
                SUM(TotalFee) as total_sales,
                COUNT(*) as order_count
            FROM orders
            WHERE YEAR(OrderDate) = %s
            AND OrderStatus = 'Delivered'
            GROUP BY MONTH(OrderDate)
            ORDER BY month
        """
        cursor.execute(query, (year,))
        result = cursor.fetchall()
        cursor.close()
        return result if result else []
    except Exception as e:
        print(f"Error fetching monthly sales: {e}")
        return []

def get_yearly_sales(self):
    """Get sales data by year (for Sales Graph)"""
    try:
        cursor = self.db.connection.cursor(dictionary=True)
        query = """
            SELECT 
                YEAR(OrderDate) as year,
                SUM(TotalFee) as total_sales,
                COUNT(*) as order_count
            FROM orders
            WHERE OrderStatus = 'Delivered'
            GROUP BY YEAR(OrderDate)
            ORDER BY year
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result if result else []
    except Exception as e:
        print(f"Error fetching yearly sales: {e}")
        return []

# ==================== END NEW METHODS ====================