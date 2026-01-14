"""
Database Schema Checker
Run this script to verify your database structure and see what columns exist
"""


def check_database_schema(db_manager):
    """Check and print database schema for debugging"""
    try:
        cursor = db_manager.connection.cursor(dictionary=True)

        print("\n" + "=" * 60)
        print("DATABASE SCHEMA CHECK")
        print("=" * 60)

        # Check Orders table structure
        print("\n📋 ORDERS TABLE STRUCTURE:")
        print("-" * 60)
        cursor.execute("DESCRIBE Orders")
        orders_columns = cursor.fetchall()

        for col in orders_columns:
            print(f"  - {col['Field']:<20} {col['Type']:<20} {col['Null']:<5} {col['Key']:<5}")

        # Check if TotalAmount exists
        has_total_amount = any(col['Field'] == 'TotalAmount' for col in orders_columns)

        if not has_total_amount:
            print("\n⚠️  WARNING: 'TotalAmount' column NOT FOUND in Orders table!")
            print("   The system will calculate totals from OrderList table instead.")
        else:
            print("\n✅ 'TotalAmount' column exists in Orders table")

        # Check OrderList table structure
        print("\n📋 ORDERLIST TABLE STRUCTURE:")
        print("-" * 60)
        cursor.execute("DESCRIBE OrderList")
        orderlist_columns = cursor.fetchall()

        for col in orderlist_columns:
            print(f"  - {col['Field']:<20} {col['Type']:<20} {col['Null']:<5} {col['Key']:<5}")

        # Check MenuItems table structure
        print("\n📋 MENUITEMS TABLE STRUCTURE:")
        print("-" * 60)
        cursor.execute("DESCRIBE MenuItems")
        menuitems_columns = cursor.fetchall()

        for col in menuitems_columns:
            print(f"  - {col['Field']:<20} {col['Type']:<20} {col['Null']:<5} {col['Key']:<5}")

        # Test revenue calculation
        print("\n💰 TESTING REVENUE CALCULATION:")
        print("-" * 60)

        # Method 1: Try TotalAmount (if exists)
        if has_total_amount:
            try:
                cursor.execute("SELECT SUM(TotalAmount) as total FROM Orders WHERE OrderStatus = 'Delivered'")
                result = cursor.fetchone()
                print(f"  Method 1 (TotalAmount): ₱{float(result['total']) if result['total'] else 0:,.2f}")
            except Exception as e:
                print(f"  Method 1 failed: {e}")

        # Method 2: Calculate from OrderList (RECOMMENDED)
        try:
            query = """
                SELECT SUM(ol.Quantity * mi.Price) as total
                FROM OrderList ol
                JOIN MenuItems mi ON ol.MenuID = mi.MenuID
                JOIN Orders o ON ol.OrderID = o.OrderID
                WHERE o.OrderStatus = 'Delivered'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"  Method 2 (OrderList calc): ₱{float(result['total']) if result['total'] else 0:,.2f}")
        except Exception as e:
            print(f"  Method 2 failed: {e}")

        # Check order counts
        print("\n📊 ORDER STATISTICS:")
        print("-" * 60)
        cursor.execute("SELECT COUNT(*) as count FROM Orders")
        result = cursor.fetchone()
        print(f"  Total Orders: {result['count']}")

        cursor.execute("SELECT COUNT(*) as count FROM Orders WHERE OrderStatus = 'Delivered'")
        result = cursor.fetchone()
        print(f"  Delivered Orders: {result['count']}")

        cursor.execute("SELECT COUNT(*) as count FROM Orders WHERE OrderStatus = 'Pending'")
        result = cursor.fetchone()
        print(f"  Pending Orders: {result['count']}")

        print("\n" + "=" * 60)
        print("SCHEMA CHECK COMPLETE")
        print("=" * 60 + "\n")

        cursor.close()

    except Exception as e:
        print(f"\n❌ Error checking database schema: {e}")
        import traceback
        traceback.print_exc()


# To use this checker, add this to your main file or run it separately:
if __name__ == "__main__":
    from Database.DatabaseManager import DatabaseManager

    # Create database connection
    db = DatabaseManager()
    if db.connect():
        check_database_schema(db)
        db.disconnect()
    else:
        print("Failed to connect to database")