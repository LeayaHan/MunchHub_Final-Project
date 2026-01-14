"""
StaffController.py - Controller for Staff Operations (FIXED VERSION)
Place this file in: Staff/StaffController.py
"""

from datetime import datetime


class StaffController:
    """Controller for staff-related operations"""

    def __init__(self, db_manager, staff_data):
        self.db_manager = db_manager
        self.staff_data = staff_data

    def get_pending_orders(self):
        """Get all pending orders (unassigned only)"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            query = """
                SELECT o.OrderID, o.TotalFee, o.DeliveryFee, o.Address, o.CustomerID,
                       CONCAT(u.UFirstName, ' ', u.ULastName) as CustomerName,
                       p.PaymentMethod,
                       GROUP_CONCAT(CONCAT(m.ItemName, ' (', ol.Quantity, ')') SEPARATOR ', ') as Items
                FROM Orders o
                JOIN Customers c ON o.CustomerID = c.CustomerID
                JOIN Users u ON c.UserID = u.UserID
                JOIN Payments p ON o.PaymentID = p.PaymentID
                JOIN OrderList ol ON o.OrderID = ol.OrderID
                JOIN MenuItems m ON ol.MenuID = m.MenuID
                WHERE o.OrderStatus = 'Pending' AND o.StaffID IS NULL
                GROUP BY o.OrderID
                ORDER BY o.OrderDate DESC
            """
            cursor.execute(query)
            orders = cursor.fetchall()
            cursor.close()
            return orders
        except Exception as e:
            print(f"Error loading pending orders: {e}")
            import traceback
            traceback.print_exc()
            return []

    def accept_order(self, order_id, notes):
        """Accept an order and assign to staff"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Get customer ID for activity log
            cursor.execute("SELECT CustomerID FROM Orders WHERE OrderID = %s", (order_id,))
            order_info = cursor.fetchone()
            if not order_info:
                cursor.close()
                return False, "Order not found"

            customer_id = order_info['CustomerID']

            # Assign staff to order and change status to Preparing
            cursor.execute(
                "UPDATE Orders SET StaffID = %s, OrderStatus = 'Preparing' WHERE OrderID = %s",
                (self.staff_data['staff_id'], order_id)
            )

            # Generate new TrackID
            cursor.execute("SELECT TrackID FROM OrderTrack ORDER BY TrackID DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                last_num = int(result['TrackID'][1:])
                new_track_id = f"T{str(last_num + 1).zfill(3)}"
            else:
                new_track_id = "T001"

            # Add to OrderTrack
            cursor.execute(
                """INSERT INTO OrderTrack (TrackID, OrderID, Notes, Status, UpdateDate)
                   VALUES (%s, %s, %s, 'Preparing', %s)""",
                (new_track_id, order_id, notes, datetime.now())
            )

            # Log activity
            self.log_staff_activity(
                cursor=cursor,
                order_id=order_id,
                customer_id=customer_id,
                action="Accepted Order",
                status="Preparing"
            )

            self.db_manager.connection.commit()
            cursor.close()
            return True, "Order accepted successfully!"

        except Exception as e:
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            print(f"Error accepting order: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)

    def mark_order_delivered(self, order_id):
        """
        🆕 NEW METHOD: Mark order as delivered by staff
        This is used when staff confirms customer received the order
        """
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Get order info
            cursor.execute("""
                SELECT o.OrderID, o.CustomerID, o.OrderStatus, o.StaffID
                FROM Orders o
                WHERE o.OrderID = %s
            """, (order_id,))

            order_info = cursor.fetchone()
            if not order_info:
                cursor.close()
                return False, "Order not found"

            # Check if this staff member is assigned to this order
            if order_info['StaffID'] != self.staff_data['staff_id']:
                cursor.close()
                return False, "You are not assigned to this order"

            # Check if order is out for delivery
            if order_info['OrderStatus'] != 'Out for delivery':
                cursor.close()
                return False, f"Order must be 'Out for delivery' to mark as delivered. Current status: {order_info['OrderStatus']}"

            # Update order status to Delivered
            cursor.execute(
                "UPDATE Orders SET OrderStatus = 'Delivered' WHERE OrderID = %s",
                (order_id,)
            )

            # Generate new TrackID
            cursor.execute("SELECT TrackID FROM OrderTrack ORDER BY TrackID DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                last_num = int(result['TrackID'][1:])
                new_track_id = f"T{str(last_num + 1).zfill(3)}"
            else:
                new_track_id = "T001"

            # Add tracking record
            cursor.execute(
                """INSERT INTO OrderTrack (TrackID, OrderID, Status, Notes, UpdateDate)
                   VALUES (%s, %s, 'Delivered', 'Confirmed by staff', %s)""",
                (new_track_id, order_id, datetime.now())
            )

            # Log activity
            self.log_staff_activity(
                cursor=cursor,
                order_id=order_id,
                customer_id=order_info['CustomerID'],
                action="Marked as Delivered",
                status="Delivered"
            )

            self.db_manager.connection.commit()
            cursor.close()
            return True, "Order marked as delivered successfully!"

        except Exception as e:
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            print(f"Error marking order as delivered: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)

    def log_staff_activity(self, cursor, order_id, customer_id, action, status):
        """Log staff activity to StaffActivityLog table"""
        try:
            # Generate new LogID
            cursor.execute("SELECT LogID FROM StaffActivityLog ORDER BY LogID DESC LIMIT 1")
            result = cursor.fetchone()

            if result:
                last_num = int(result['LogID'][1:])
                new_log_id = f"L{str(last_num + 1).zfill(3)}"
            else:
                new_log_id = "L001"

            # Insert activity log
            insert_query = """
                INSERT INTO StaffActivityLog 
                (LogID, StaffID, OrderID, CustomerID, Action, Status, ActivityDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                new_log_id,
                self.staff_data['staff_id'],
                order_id,
                customer_id,
                action,
                status,
                datetime.now()
            ))

            print(f"✅ Staff activity logged: {new_log_id} - {action}")

        except Exception as e:
            print(f"⚠️ Warning: Failed to log staff activity: {e}")

    def get_activity_log(self):
        """Get activity log for this staff member"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            query = """
                SELECT sal.LogID, sal.OrderID, sal.Action, sal.Status, sal.ActivityDate,
                       CONCAT(u.UFirstName, ' ', u.ULastName) as CustomerName,
                       c.CustomerID
                FROM StaffActivityLog sal
                JOIN Orders o ON sal.OrderID = o.OrderID
                JOIN Customers c ON sal.CustomerID = c.CustomerID
                JOIN Users u ON c.UserID = u.UserID
                WHERE sal.StaffID = %s
                ORDER BY sal.ActivityDate DESC
                LIMIT 50
            """
            cursor.execute(query, (self.staff_data['staff_id'],))
            activities = cursor.fetchall()
            cursor.close()
            return activities
        except Exception as e:
            print(f"Error loading activity log: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_track_orders(self):
        """
        🔧 FIXED: Get ONLY ACTIVE tracking records (excludes Delivered and Cancelled)
        Delivered orders are removed from tracking page automatically!
        """
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Only show orders that are NOT delivered or cancelled
            query = """
                SELECT DISTINCT
                    ot.TrackID, 
                    ot.OrderID, 
                    ot.Status, 
                    ot.Notes, 
                    ot.UpdateDate,
                    o.OrderStatus, 
                    o.StaffID
                FROM OrderTrack ot
                JOIN Orders o ON ot.OrderID = o.OrderID
                WHERE o.StaffID = %s
                  AND o.OrderStatus NOT IN ('Delivered', 'Cancelled')
                ORDER BY ot.UpdateDate DESC
            """

            cursor.execute(query, (self.staff_data['staff_id'],))
            tracks = cursor.fetchall()
            cursor.close()

            print(f"✅ Loaded {len(tracks)} ACTIVE tracking records for staff {self.staff_data['staff_id']}")
            return tracks

        except Exception as e:
            print(f"Error loading track orders: {e}")
            import traceback
            traceback.print_exc()
            return []

    def update_track(self, track_id, new_status, new_notes):
        """Update a tracking record"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # Get order info before updating
            cursor.execute("""
                SELECT ot.OrderID, o.CustomerID
                FROM OrderTrack ot
                JOIN Orders o ON ot.OrderID = o.OrderID
                WHERE ot.TrackID = %s
            """, (track_id,))

            track_info = cursor.fetchone()
            if not track_info:
                cursor.close()
                return False, "Track record not found"

            # Update tracking record
            cursor.execute(
                """UPDATE OrderTrack 
                   SET Status = %s, Notes = %s, UpdateDate = %s
                   WHERE TrackID = %s""",
                (new_status, new_notes, datetime.now(), track_id)
            )

            # Update order status if tracking status changes
            status_map = {
                'Confirmed': 'Pending',
                'Preparing': 'Preparing',
                'Ready': 'Preparing',
                'Out for Delivery': 'Out for delivery',
                'Delivered': 'Delivered',
                'Cancelled': 'Cancelled'
            }

            order_status = status_map.get(new_status, new_status)
            cursor.execute(
                "UPDATE Orders SET OrderStatus = %s WHERE OrderID = %s",
                (order_status, track_info['OrderID'])
            )

            # Log activity
            action_text = f"Updated order status to {new_status}"
            self.log_staff_activity(
                cursor=cursor,
                order_id=track_info['OrderID'],
                customer_id=track_info['CustomerID'],
                action=action_text,
                status=order_status
            )

            self.db_manager.connection.commit()
            cursor.close()
            return True, "Tracking updated successfully!"

        except Exception as e:
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            print(f"Error updating track: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)