"""
DebugHelper.py - Helper to debug and verify category filtering
Place this file in: Customer/DebugHelper.py

Run this to check your database and verify categories are correct
"""


def verify_menu_categories(db_manager):
    """Verify that menu items are correctly assigned to categories"""
    try:
        cursor = db_manager.connection.cursor(dictionary=True)

        print("\n" + "=" * 70)
        print("CATEGORY AND MENU ITEM VERIFICATION")
        print("=" * 70)

        # Get all categories
        cursor.execute("""
            SELECT CategoryID, CategoryName, Description 
            FROM Categories 
            ORDER BY CategoryName
        """)
        categories = cursor.fetchall()

        print(f"\n📁 Found {len(categories)} categories:\n")

        for cat in categories:
            print(f"   {cat['CategoryID']}: {cat['CategoryName']}")
            if cat['Description']:
                print(f"      └─ {cat['Description']}")

        print("\n" + "-" * 70)

        # Get all menu items with their categories
        cursor.execute("""
            SELECT m.MenuID, m.ItemName, m.CategoryID, c.CategoryName, m.Price, m.isAvailable
            FROM MenuItems m
            JOIN Categories c ON m.CategoryID = c.CategoryID
            ORDER BY c.CategoryName, m.ItemName
        """)
        items = cursor.fetchall()

        print(f"\n🍽️  Menu Items by Category:\n")

        current_category = None
        category_counts = {}

        for item in items:
            cat_name = item['CategoryName']

            if cat_name != current_category:
                if current_category:
                    print()  # Add space between categories
                current_category = cat_name
                category_counts[cat_name] = 0
                print(f"\n📂 {cat_name.upper()}")
                print("   " + "-" * 60)

            status = "✓ Available" if item['isAvailable'] else "✗ Unavailable"
            print(f"   • {item['ItemName']:30} (ID: {item['MenuID']})  ₱{float(item['Price']):>7.2f}  {status}")

            if item['isAvailable']:
                category_counts[cat_name] += 1

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        total_available = sum(category_counts.values())
        print(f"\n📊 Total Available Items: {total_available}")
        print(f"\n   Items per Category:")
        for cat_name, count in sorted(category_counts.items()):
            print(f"      • {cat_name}: {count} item{'s' if count != 1 else ''}")

        # Check for orphaned items
        cursor.execute("""
            SELECT m.MenuID, m.ItemName, m.CategoryID
            FROM MenuItems m
            LEFT JOIN Categories c ON m.CategoryID = c.CategoryID
            WHERE c.CategoryID IS NULL
        """)
        orphans = cursor.fetchall()

        if orphans:
            print(f"\n⚠️  WARNING: Found {len(orphans)} orphaned items (items with invalid CategoryID):")
            for item in orphans:
                print(f"      • {item['ItemName']} (MenuID: {item['MenuID']}, CategoryID: {item['CategoryID']})")
        else:
            print("\n✅ All menu items are properly assigned to valid categories!")

        print("\n" + "=" * 70 + "\n")

        cursor.close()
        return True

    except Exception as e:
        print(f"\n❌ Error verifying categories: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_category_filtering(db_manager):
    """Test the category filtering logic"""
    try:
        from Customer.MenuModel import MenuModel

        print("\n" + "=" * 70)
        print("TESTING CATEGORY FILTERING")
        print("=" * 70)

        model = MenuModel(db_manager)

        # Load data
        print("\n1. Loading categories...")
        success, categories = model.load_categories()
        if success:
            print(f"   ✓ Loaded {len(categories)} categories")
        else:
            print("   ✗ Failed to load categories")
            return False

        print("\n2. Loading menu items...")
        success, items = model.load_all_menu_items()
        if success:
            print(f"   ✓ Loaded {len(items)} menu items")
        else:
            print("   ✗ Failed to load menu items")
            return False

        # Test filtering
        print("\n3. Testing category filters:\n")

        # Test "All" filter
        all_items = model.filter_by_category('all')
        print(f"   • 'All Items' filter: {len(all_items)} items")

        # Test each category
        for cat in categories:
            filtered = model.filter_by_category(cat['CategoryID'])
            print(f"   • '{cat['CategoryName']}' filter: {len(filtered)} items")

            # Show first 3 items in each category
            if filtered:
                for item in filtered[:3]:
                    print(f"       └─ {item['ItemName']}")
                if len(filtered) > 3:
                    print(f"       └─ ... and {len(filtered) - 3} more")

        print("\n" + "=" * 70 + "\n")
        return True

    except Exception as e:
        print(f"\n❌ Error testing filtering: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n⚠️  This is a helper module. Import it in your main file to use.")
    print("Example usage:")
    print("""
    from Customer.DebugHelper import verify_menu_categories, test_category_filtering

    # After connecting to database:
    verify_menu_categories(db_manager)
    test_category_filtering(db_manager)
    """)