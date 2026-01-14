"""
MenuModel.py - Model for Menu and Category Data
Place this file in: Customer/MenuModel.py
"""


class MenuModel:
    """Model class for managing menu and category data"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.categories = []
        self.menu_items = []
        self.filtered_items = []

    def load_categories(self):
        """Load all categories from database"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)
            query = """
                SELECT DISTINCT c.CategoryID, c.CategoryName, c.Description
                FROM Categories c
                INNER JOIN MenuItems m ON c.CategoryID = m.CategoryID
                WHERE m.isAvailable = 1
                ORDER BY c.CategoryName
            """
            cursor.execute(query)
            self.categories = cursor.fetchall()
            cursor.close()
            return True, self.categories
        except Exception as e:
            print(f"Error loading categories: {e}")
            return False, []

    def load_all_menu_items(self):
        """Load all available menu items from database"""
        try:
            cursor = self.db_manager.connection.cursor(dictionary=True)

            # First, check if Description column exists
            cursor.execute("SHOW COLUMNS FROM MenuItems LIKE 'Description'")
            has_description = cursor.fetchone() is not None

            # Build query based on column availability - FIXED: Use correct table alias
            if has_description:
                query = """
                    SELECT m.MenuID, m.ItemName, m.Price, m.Description, 
                           m.isAvailable, c.CategoryName, c.CategoryID
                    FROM MenuItems m
                    JOIN Categories c ON m.CategoryID = c.CategoryID
                    WHERE m.isAvailable = 1
                    ORDER BY c.CategoryName, m.ItemName
                """
            else:
                query = """
                    SELECT m.MenuID, m.ItemName, m.Price, 
                           m.isAvailable, c.CategoryName, c.CategoryID
                    FROM MenuItems m
                    JOIN Categories c ON m.CategoryID = c.CategoryID
                    WHERE m.isAvailable = 1
                    ORDER BY c.CategoryName, m.ItemName
                """

            cursor.execute(query)
            self.menu_items = cursor.fetchall()

            # Add empty Description field if it doesn't exist in database
            if not has_description:
                for item in self.menu_items:
                    item['Description'] = None

            self.filtered_items = self.menu_items.copy()
            cursor.close()
            return True, self.menu_items
        except Exception as e:
            print(f"Error loading menu items: {e}")
            import traceback
            traceback.print_exc()
            return False, []

    def filter_by_category(self, category_id=None):
        """Filter menu items by category"""
        if category_id is None or category_id == 'all':
            self.filtered_items = self.menu_items.copy()
        else:
            self.filtered_items = [
                item for item in self.menu_items
                if item['CategoryID'] == category_id
            ]
        return self.filtered_items

    def search_menu_items(self, search_text):
        """Search menu items by name"""
        if not search_text:
            self.filtered_items = self.menu_items.copy()
        else:
            search_lower = search_text.lower()
            self.filtered_items = [
                item for item in self.menu_items
                if search_lower in item['ItemName'].lower()
            ]
        return self.filtered_items

    def get_item_by_id(self, menu_id):
        """Get a specific menu item by ID"""
        for item in self.menu_items:
            if item['MenuID'] == menu_id:
                return item
        return None

    def get_category_count(self, category_id):
        """Get count of items in a category"""
        count = sum(1 for item in self.menu_items if item['CategoryID'] == category_id)
        return count