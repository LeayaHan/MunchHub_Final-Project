"""
CartModel.py - Model for Shopping Cart
FIXED: Changed Decimal to float for compatibility with display widgets
"""


class CartModel:
    """Model class for managing shopping cart"""

    def __init__(self):
        self.cart_items = []
        self.delivery_fee = 50.00  # CHANGED: float instead of Decimal

    def add_item(self, menu_item):
        """Add item to cart or increase quantity if already exists"""
        # Check if item already in cart
        for cart_item in self.cart_items:
            if cart_item['menu_id'] == menu_item['MenuID']:
                cart_item['quantity'] += 1
                cart_item['subtotal'] = float(menu_item['Price']) * cart_item['quantity']  # CHANGED: float
                return True

        # Add new item to cart
        new_item = {
            'menu_id': menu_item['MenuID'],
            'name': menu_item['ItemName'],
            'price': float(menu_item['Price']),  # CHANGED: float instead of Decimal
            'quantity': 1,
            'subtotal': float(menu_item['Price'])  # CHANGED: float instead of Decimal
        }
        self.cart_items.append(new_item)
        return True

    def remove_item(self, cart_item):
        """Remove item from cart"""
        if cart_item in self.cart_items:
            self.cart_items.remove(cart_item)
            return True
        return False

    def update_quantity(self, cart_item, quantity):
        """Update item quantity"""
        if quantity <= 0:
            return self.remove_item(cart_item)

        cart_item['quantity'] = quantity
        cart_item['subtotal'] = cart_item['price'] * quantity
        return True

    def increase_quantity(self, cart_item):
        """Increase item quantity by 1"""
        cart_item['quantity'] += 1
        cart_item['subtotal'] = cart_item['price'] * cart_item['quantity']

    def decrease_quantity(self, cart_item):
        """Decrease item quantity by 1"""
        if cart_item['quantity'] > 1:
            cart_item['quantity'] -= 1
            cart_item['subtotal'] = cart_item['price'] * cart_item['quantity']
            return True
        return False

    def get_subtotal(self):
        """Calculate cart subtotal"""
        return sum(item['subtotal'] for item in self.cart_items)

    def get_total(self):
        """Calculate total including delivery fee"""
        return self.get_subtotal() + self.delivery_fee

    def get_item_count(self):
        """Get total number of items in cart"""
        return len(self.cart_items)

    def clear_cart(self):
        """Clear all items from cart"""
        self.cart_items.clear()

    def is_empty(self):
        """Check if cart is empty"""
        return len(self.cart_items) == 0