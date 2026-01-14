"""
CustomerController.py - Controller for Customer Operations with Tax
Place this file in: Customer/CustomerController.py
"""

from PyQt6.QtWidgets import QMessageBox
from decimal import Decimal


class CustomerController:
    """Controller class for handling customer operations"""

    # Tax rate constant (12% VAT)
    TAX_RATE = 0.12

    def __init__(self, menu_model, cart_model, db_manager, user_data):
        self.menu_model = menu_model
        self.cart_model = cart_model
        self.db_manager = db_manager
        self.user_data = user_data

    def calculate_tax(self, amount):
        """Calculate tax for given amount"""
        return round(float(amount) * self.TAX_RATE, 2)

    def initialize_data(self):
        """Initialize menu and category data"""
        # Load categories
        cat_success, categories = self.menu_model.load_categories()
        if not cat_success:
            return False, "Failed to load categories"

        # Load menu items
        menu_success, menu_items = self.menu_model.load_all_menu_items()
        if not menu_success:
            return False, "Failed to load menu items"

        return True, "Data loaded successfully"

    def filter_menu_by_category(self, category_id):
        """Filter menu items by category"""
        filtered_items = self.menu_model.filter_by_category(category_id)
        return filtered_items

    def search_menu(self, search_text):
        """Search menu items"""
        results = self.menu_model.search_menu_items(search_text)
        return results

    def add_to_cart(self, menu_item):
        """Add item to cart"""
        success = self.cart_model.add_item(menu_item)
        return success

    def remove_from_cart(self, cart_item):
        """Remove item from cart"""
        return self.cart_model.remove_item(cart_item)

    def update_cart_quantity(self, cart_item, change):
        """Update cart item quantity"""
        if change > 0:
            self.cart_model.increase_quantity(cart_item)
        else:
            if not self.cart_model.decrease_quantity(cart_item):
                self.cart_model.remove_item(cart_item)

    def get_cart_summary(self):
        """Get cart summary data"""
        return {
            'items': self.cart_model.cart_items,
            'subtotal': self.cart_model.get_subtotal(),
            'delivery_fee': self.cart_model.delivery_fee,
            'total': self.cart_model.get_total(),
            'item_count': self.cart_model.get_item_count(),
            'is_empty': self.cart_model.is_empty()
        }

    def place_order(self, order_details):
        """Place order in database with tax calculation"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Generate OrderID
            cursor.execute("SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1")
            last_order = cursor.fetchone()
            new_order_id = f"O{str(int(last_order['OrderID'][1:]) + 1).zfill(3)}" if last_order else "O001"

            print(f"Generated OrderID: {new_order_id}")

            # Get or create PaymentID
            cursor.execute("SELECT PaymentID FROM Payments WHERE PaymentMethod = %s LIMIT 1",
                          (order_details['payment_method'],))
            payment = cursor.fetchone()

            if not payment:
                cursor.execute("SELECT PaymentID FROM Payments ORDER BY PaymentID DESC LIMIT 1")
                last_payment = cursor.fetchone()
                payment_id = f"P{str(int(last_payment['PaymentID'][1:]) + 1).zfill(3)}" if last_payment else "P001"
                cursor.execute("INSERT INTO Payments (PaymentID, PaymentMethod) VALUES (%s, %s)",
                             (payment_id, order_details['payment_method']))
            else:
                payment_id = payment['PaymentID']

            # Calculate totals WITH TAX
            subtotal = self.cart_model.get_subtotal()
            tax = order_details.get('tax', self.calculate_tax(subtotal))  # Get from order_details or calculate
            delivery_fee = self.cart_model.delivery_fee
            total_fee = subtotal + tax + delivery_fee

            print(f"Order totals - Subtotal: ₱{subtotal:.2f}, Tax: ₱{tax:.2f}, Delivery: ₱{delivery_fee:.2f}, Total: ₱{total_fee:.2f}")

            # Insert order WITH TAX COLUMN
            # First, check if Tax column exists in database
            cursor.execute("SHOW COLUMNS FROM Orders LIKE 'Tax'")
            tax_column_exists = cursor.fetchone()

            if tax_column_exists:
                # Tax column exists - use it
                cursor.execute("""
                    INSERT INTO Orders (OrderID, CustomerID, StaffID, PaymentID, Address, TotalFee, Tax, DeliveryFee, OrderStatus)
                    VALUES (%s, %s, NULL, %s, %s, %s, %s, %s, 'Pending')
                """, (new_order_id, self.user_data['customer_id'], payment_id, order_details['address'],
                      total_fee, tax, delivery_fee))
                print(f"Order inserted with Tax column: ₱{tax:.2f}")
            else:
                # Tax column doesn't exist - insert without it (backward compatibility)
                cursor.execute("""
                    INSERT INTO Orders (OrderID, CustomerID, StaffID, PaymentID, Address, TotalFee, DeliveryFee, OrderStatus)
                    VALUES (%s, %s, NULL, %s, %s, %s, %s, 'Pending')
                """, (new_order_id, self.user_data['customer_id'], payment_id, order_details['address'],
                      total_fee, delivery_fee))
                print(f"WARNING: Tax column not found in database. Order inserted without tax tracking.")
                print(f"Please run: ALTER TABLE Orders ADD COLUMN Tax DECIMAL(10,2) NOT NULL DEFAULT 0.00 AFTER DeliveryFee;")

            print(f"Order {new_order_id} inserted successfully")

            # Check if there are any existing OrderListIDs for this OrderID (should be none for new order)
            cursor.execute("SELECT OrderListID FROM OrderList WHERE OrderID = %s", (new_order_id,))
            existing_items = cursor.fetchall()
            if existing_items:
                print(f"WARNING: Found existing items for new order {new_order_id}: {existing_items}")
                # This shouldn't happen - clean up
                cursor.execute("DELETE FROM OrderList WHERE OrderID = %s", (new_order_id,))
                print(f"Cleaned up existing items for {new_order_id}")

            # Insert order items with unique OrderListIDs
            # IMPORTANT: OrderListID is varchar(5), so format must be O1L1 (5 chars max)
            for index, item in enumerate(self.cart_model.cart_items, start=1):
                # Extract order number without leading zeros (O007 -> 7)
                order_num = int(new_order_id[1:])  # Remove 'O' and convert to int

                # Format: O{num}L{item} - keeps it under 5 characters
                # Examples: O1L1, O1L2, O7L1, O12L3
                orderlist_id = f"O{order_num}L{index}"

                print(f"Creating OrderListID: '{orderlist_id}' (length={len(orderlist_id)}) for item '{item['name']}'")

                # Verify length is 5 or less
                if len(orderlist_id) > 5:
                    raise Exception(f"OrderListID '{orderlist_id}' exceeds 5 character limit! Order has too many items or order number is too high.")

                # Double-check this ID doesn't exist
                cursor.execute("SELECT OrderListID FROM OrderList WHERE OrderListID = %s", (orderlist_id,))
                existing = cursor.fetchone()

                if existing:
                    error_msg = f"CRITICAL: OrderListID '{orderlist_id}' already exists!"
                    print(error_msg)
                    raise Exception(error_msg)

                # Insert the order item
                try:
                    cursor.execute("""
                        INSERT INTO OrderList (OrderListID, OrderID, MenuID, Quantity, SubTotal)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (orderlist_id, new_order_id, item['menu_id'], item['quantity'], item['subtotal']))

                    print(f"✓ Successfully inserted OrderListID: '{orderlist_id}'")

                except Exception as insert_error:
                    print(f"✗ Failed to insert OrderListID: '{orderlist_id}'")
                    print(f"Error details: {insert_error}")
                    raise

            # Create initial order track entry
            cursor.execute("SELECT TrackID FROM OrderTrack ORDER BY TrackID DESC LIMIT 1")
            last_track = cursor.fetchone()
            track_id = f"T{str(int(last_track['TrackID'][1:]) + 1).zfill(3)}" if last_track else "T001"

            cursor.execute("""
                INSERT INTO OrderTrack (TrackID, OrderID, Status, Notes)
                VALUES (%s, %s, 'Confirmed', 'Order placed successfully')
            """, (track_id, new_order_id))

            self.db_manager.connection.commit()
            cursor.close()

            print(f"✓ Order {new_order_id} completed successfully!")
            print(f"  - Subtotal: ₱{subtotal:.2f}")
            print(f"  - Tax (12%): ₱{tax:.2f}")
            print(f"  - Delivery: ₱{delivery_fee:.2f}")
            print(f"  - Total: ₱{total_fee:.2f}")

            # Clear cart after successful order
            self.cart_model.clear_cart()

            return True, new_order_id, "Order placed successfully"

        except Exception as e:
            if self.db_manager and self.db_manager.connection:
                self.db_manager.connection.rollback()
            print(f"✗ Order error: {e}")
            import traceback
            traceback.print_exc()

            # Check database state
            try:
                cursor = self.db_manager.connection.cursor(dictionary=True)
                cursor.execute("SELECT OrderListID FROM OrderList WHERE OrderListID LIKE 'O%L%'")
                results = cursor.fetchall()
                print(f"Current OrderList entries: {len(results)} records")
                cursor.close()
            except:
                pass

            return False, None, f"Failed to place order: {str(e)}"

    def get_order_history(self):
        """Get customer's order history with tax information"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Check if Tax column exists
            cursor.execute("SHOW COLUMNS FROM Orders LIKE 'Tax'")
            tax_column_exists = cursor.fetchone()

            if tax_column_exists:
                # Tax column exists - include it in query
                query = """
                    SELECT o.OrderID, o.TotalFee, o.Tax, o.DeliveryFee, o.OrderStatus, 
                           o.Address, p.PaymentMethod,
                           (SELECT MIN(ot.UpdateDate) 
                            FROM OrderTrack ot 
                            WHERE ot.OrderID = o.OrderID) as OrderDate
                    FROM Orders o
                    JOIN Payments p ON o.PaymentID = p.PaymentID
                    WHERE o.CustomerID = %s
                    ORDER BY o.OrderID DESC
                """
            else:
                # Tax column doesn't exist - calculate it from TotalFee
                query = """
                    SELECT o.OrderID, o.TotalFee, 
                           ROUND((o.TotalFee - o.DeliveryFee) * 0.12 / 1.12, 2) as Tax,
                           o.DeliveryFee, o.OrderStatus, 
                           o.Address, p.PaymentMethod,
                           (SELECT MIN(ot.UpdateDate) 
                            FROM OrderTrack ot 
                            WHERE ot.OrderID = o.OrderID) as OrderDate
                    FROM Orders o
                    JOIN Payments p ON o.PaymentID = p.PaymentID
                    WHERE o.CustomerID = %s
                    ORDER BY o.OrderID DESC
                """

            cursor.execute(query, (self.user_data['customer_id'],))
            orders = cursor.fetchall()
            cursor.close()
            return True, orders
        except Exception as e:
            print(f"Error loading order history: {e}")
            return False, []