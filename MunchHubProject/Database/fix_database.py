import mysql.connector


def cleanup_database():
    """Clean up database and change to MENU1, MENU2, MENU3 format"""

    # Connect to database
    try:
        db = mysql.connector.connect(
            host='localhost',
            database='munchhubdb',
            user='root',
            password=''
        )
        cursor = db.cursor(dictionary=True)

        print("=" * 60)
        print("MUNCHHUB DATABASE CLEANUP - Change to MENU1, MENU2, MENU3")
        print("=" * 60)

        # Step 1: Check current state
        print("\n1. CHECKING CURRENT MENU ITEMS:")
        print("-" * 60)
        cursor.execute("SELECT MenuID, ItemName FROM MenuItems ORDER BY MenuID")
        items = cursor.fetchall()

        if items:
            for item in items:
                print(f"   {item['MenuID']} - {item['ItemName']}")
        else:
            print("   No menu items found.")

        # Step 2: Check if any items are in orders
        print("\n2. CHECKING ORDER REFERENCES:")
        print("-" * 60)
        cursor.execute("SELECT DISTINCT MenuID FROM OrderList")
        orders = cursor.fetchall()

        if orders:
            print("   ⚠ WARNING: Following items are in orders:")
            for order in orders:
                print(f"   - {order['MenuID']}")
            print("   Cannot update these items due to foreign key constraints!")

            response = input("\n   Delete all test orders and menu items? (yes/no): ")
            if response.lower() != 'yes':
                print("\n   ✗ Cleanup cancelled.")
                cursor.close()
                db.close()
                return
        else:
            print("   ✓ No order references found. Safe to proceed.")

        # Step 3: Delete old items
        print("\n3. DELETING OLD MENU ITEMS:")
        print("-" * 60)

        # Delete from OrderList first (if any)
        cursor.execute("DELETE FROM OrderList")
        deleted_orders = cursor.rowcount
        print(f"   Deleted {deleted_orders} order list entries")

        # Delete from MenuItems
        cursor.execute("SELECT MenuID, ItemName FROM MenuItems")
        items_to_delete = cursor.fetchall()

        cursor.execute("DELETE FROM MenuItems")
        deleted_items = cursor.rowcount
        print(f"   Deleted {deleted_items} menu items")

        if items_to_delete:
            for item in items_to_delete:
                print(f"   - {item['MenuID']} ({item['ItemName']})")

        # Commit deletions
        db.commit()

        # Step 4: Ask if user wants to add sample data
        print("\n4. ADD SAMPLE MENU ITEMS (OPTIONAL):")
        print("-" * 60)
        add_samples = input("   Add sample menu items with MENU1, MENU2, format? (yes/no): ")

        if add_samples.lower() == 'yes':
            sample_items = [
                ('MENU1', 'CAT01', 'Sinigang', 190.00, 1),
                ('MENU2', 'CAT01', 'Adobo', 150.00, 1),
                ('MENU3', 'CAT01', 'Kare-Kare', 200.00, 1),
                ('MENU4', 'CAT02', 'Halo-Halo', 80.00, 1),
                ('MENU5', 'CAT02', 'Leche Flan', 70.00, 1),
                ('MENU6', 'CAT03', 'Lumpia', 120.00, 1),
                ('MENU7', 'CAT04', 'Chicharon', 50.00, 1),
            ]

            inserted = 0
            for menu_id, cat_id, name, price, available in sample_items:
                try:
                    cursor.execute("""
                        INSERT INTO MenuItems (MenuID, CategoryID, ItemName, Price, isAvailable)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (menu_id, cat_id, name, price, available))
                    print(f"   ✓ Added: {menu_id} - {name}")
                    inserted += 1
                except Exception as e:
                    print(f"   ✗ Failed to add {menu_id}: {e}")

            db.commit()
            print(f"\n   Total added: {inserted} items")

        # Step 5: Show final state
        print("\n5. FINAL DATABASE STATE:")
        print("-" * 60)
        cursor.execute("""
            SELECT m.MenuID, m.ItemName, c.CategoryName, m.Price, m.isAvailable
            FROM MenuItems m
            JOIN Categories c ON m.CategoryID = c.CategoryID
            ORDER BY CAST(SUBSTRING(m.MenuID, 5) AS UNSIGNED)
        """)
        final_items = cursor.fetchall()

        if final_items:
            print(f"\n   {'Menu ID':<12} {'Item Name':<20} {'Category':<15} {'Price':<10} {'Available'}")
            print(f"   {'-' * 12} {'-' * 20} {'-' * 15} {'-' * 10} {'-' * 9}")
            for item in final_items:
                available = "Yes" if item['isAvailable'] else "No"
                print(
                    f"   {item['MenuID']:<12} {item['ItemName']:<20} {item['CategoryName']:<15} ₱{item['Price']:<9.2f} {available}")
        else:
            print("   No menu items in database.")

        # Close connection
        cursor.close()
        db.close()

        print("\n" + "=" * 60)
        print("✅ DATABASE CLEANUP COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Restart your application")
        print("2. Try adding a new menu item")
        print("3. It should generate MENU1, MENU2, MENU3, etc.")
        print("=" * 60)

    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        if db:
            db.rollback()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


if __name__ == "__main__":
    cleanup_database()