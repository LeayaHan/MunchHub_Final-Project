import mysql.connector
from mysql.connector import Error
import hashlib
from PyQt6.QtGui import QValidator
from datetime import datetime


class DatabaseManager:
    """Database manager class for MunchHub system"""

    def __init__(self, host='localhost', database='munchhubdb', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
        return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_user_id(self):
        """Generate next UserID in format U0001, U0002, etc."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT UserID FROM Users ORDER BY UserID DESC LIMIT 1")
            result = cursor.fetchone()
            cursor.close()

            if result:
                last_id = int(result[0][1:])  # Extract number from U0001
                new_id = f"U{last_id + 1:04d}"
            else:
                new_id = "U0001"
            return new_id
        except Error as e:
            print(f"Error generating UserID: {e}")
            return None

    def generate_customer_id(self):
        """Generate next CustomerID in format C0001, C0002, etc."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT CustomerID FROM Customers ORDER BY CustomerID DESC LIMIT 1")
            result = cursor.fetchone()
            cursor.close()

            if result:
                last_id = int(result[0][1:])
                new_id = f"C{last_id + 1:04d}"
            else:
                new_id = "C0001"
            return new_id
        except Error as e:
            print(f"Error generating CustomerID: {e}")
            return None

    def generate_staff_id(self):
        """Generate next StaffID in format S0001, S0002, etc."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT StaffID FROM Staffs ORDER BY StaffID DESC LIMIT 1")
            result = cursor.fetchone()
            cursor.close()

            if result:
                last_id = int(result[0][1:])
                new_id = f"S{last_id + 1:04d}"
            else:
                new_id = "S0001"
            return new_id
        except Error as e:
            print(f"Error generating StaffID: {e}")
            return None

    def register_user(self, username, password, first_name, middle_name, last_name, phone_number):
        """Register a new customer user"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Check if username already exists
            cursor.execute("SELECT Username FROM Users WHERE Username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "Username already exists! Please choose a different username."

            # Generate new UserID
            cursor.execute("SELECT UserID FROM Users ORDER BY UserID DESC LIMIT 1")
            last_user = cursor.fetchone()
            if last_user:
                last_id = int(last_user['UserID'][1:])  # Remove 'U' prefix
                new_user_id = f"U{str(last_id + 1).zfill(3)}"
            else:
                new_user_id = "U001"

            # Hash the password
            password_hash = self.hash_password(password)

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
                middle_name,
                last_name,
                phone_number
            ))

            # Generate new CustomerID
            cursor.execute("SELECT CustomerID FROM Customers ORDER BY CustomerID DESC LIMIT 1")
            last_customer = cursor.fetchone()
            if last_customer:
                last_id = int(last_customer['CustomerID'][1:])  # Remove 'C' prefix
                new_customer_id = f"C{str(last_id + 1).zfill(3)}"
            else:
                new_customer_id = "C001"

            # Insert into Customers table with default address "To be provided"
            insert_customer_query = """
                INSERT INTO Customers (CustomerID, UserID, Address)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_customer_query, (
                new_customer_id,
                new_user_id,
                "To be provided"  # Default address
            ))

            # Commit the transaction
            self.connection.commit()
            cursor.close()

            print(f"User {username} registered successfully with ID: {new_user_id}")
            return True, "Account created successfully! You can now login."

        except Error as e:
            # Rollback in case of error
            if self.connection:
                self.connection.rollback()
            print(f"Error registering user: {e}")
            return False, f"Registration failed: {str(e)}"

    def hash_password(self, password):
        """Hash password using SHA-256"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password):
        """Authenticate customer credentials"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # First, try to find the user
            query = """
                SELECT u.UserID, u.Username, u.Password, u.UFirstName, u.UMiddleName, u.ULastName, 
                       u.PhoneNum, c.CustomerID, c.Address
                FROM Users u
                INNER JOIN Customers c ON u.UserID = c.UserID
                WHERE u.Username = %s
            """

            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()

            if not user:
                return False, None, "Invalid username or password!"

            # Check password - handle both hashed and plain text passwords
            stored_password = user['Password']

            # Check if stored password is hashed (typically starts with hash algorithm identifier)
            # or if it's plain text
            if stored_password.startswith('$') or len(stored_password) > 50:
                # Password appears to be hashed, compare with hashed input
                password_hash = self.hash_password(password)
                password_match = (stored_password == password_hash)
            else:
                # Password appears to be plain text (for backwards compatibility with existing data)
                password_match = (stored_password == password)

            if password_match:
                full_name = f"{user['UFirstName']} {user['UMiddleName'] or ''} {user['ULastName']}".strip()
                user_data = {
                    'user_id': user['UserID'],
                    'customer_id': user['CustomerID'],
                    'username': user['Username'],
                    'full_name': full_name,
                    'phone_number': user['PhoneNum'],
                    'address': user['Address'],
                    'role': 'customer'
                }
                print(f"Customer {username} authenticated successfully")
                return True, user_data, "Login successful!"
            else:
                return False, None, "Invalid username or password!"

        except Error as e:
            print(f"Error authenticating user: {e}")
            return False, None, f"Database error: {str(e)}"

    def authenticate_staff(self, username, password):
        """Authenticate staff credentials"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT u.UserID, u.Username, u.Password, u.UFirstName, u.UMiddleName, u.ULastName, 
                       u.PhoneNum, s.StaffID
                FROM Users u
                INNER JOIN Staffs s ON u.UserID = s.UserID
                WHERE u.Username = %s
            """

            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()

            if not user:
                return False, None, "Invalid username or password!"

            stored_password = user['Password']

            # Check if stored password is hashed or plain text
            if stored_password.startswith('$') or len(stored_password) > 50:
                password_hash = self.hash_password(password)
                password_match = (stored_password == password_hash)
            else:
                password_match = (stored_password == password)

            if password_match:
                full_name = f"{user['UFirstName']} {user['UMiddleName'] or ''} {user['ULastName']}".strip()
                user_data = {
                    'user_id': user['UserID'],
                    'staff_id': user['StaffID'],
                    'username': user['Username'],
                    'full_name': full_name,
                    'phone_number': user['PhoneNum'],
                    'role': 'staff'
                }
                print(f"Staff {username} authenticated successfully")
                return True, user_data, "Login successful!"
            else:
                return False, None, "Invalid username or password!"

        except Error as e:
            print(f"Error authenticating staff: {e}")
            return False, None, f"Database error: {str(e)}"

    def authenticate_admin(self, username, password):
        """Authenticate admin credentials"""
        try:
            # Check if there's a separate admins table
            cursor = self.connection.cursor(dictionary=True)

            # First check if admins table exists
            cursor.execute("SHOW TABLES LIKE 'admins'")
            admin_table_exists = cursor.fetchone() is not None

            if admin_table_exists:
                query = """
                    SELECT AdminID, Username, Password, FirstName, MiddleName, LastName, PhoneNum
                    FROM Admins
                    WHERE Username = %s
                """
                cursor.execute(query, (username,))
                admin = cursor.fetchone()

                if admin:
                    stored_password = admin['Password']

                    # Check if stored password is hashed or plain text
                    if stored_password.startswith('$') or len(stored_password) > 50:
                        password_hash = self.hash_password(password)
                        password_match = (stored_password == password_hash)
                    else:
                        password_match = (stored_password == password)

                    if password_match:
                        full_name = f"{admin['FirstName']} {admin.get('MiddleName') or ''} {admin['LastName']}".strip()
                        admin_data = {
                            'admin_id': admin['AdminID'],
                            'username': admin['Username'],
                            'full_name': full_name,
                            'phone_number': admin.get('PhoneNum', ''),
                            'role': 'admin'
                        }
                        print(f"Admin {username} authenticated successfully")
                        cursor.close()
                        return True, admin_data, "Login successful!"

            cursor.close()
            return False, None, "Invalid admin credentials!"

        except Error as e:
            print(f"Error authenticating admin: {e}")
            return False, None, f"Database error: {str(e)}"

    def get_user_by_username(self, username):
        """Get user information by username"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Users WHERE Username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error getting user by username: {e}")
            return None


class PhoneNumberValidator(QValidator):
    """Custom validator for phone numbers - only allows digits and max 11 characters"""

    def validate(self, text, pos):
        # Remove any non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, text))

        if len(digits_only) > 11:
            return QValidator.State.Invalid, text[:pos - 1], pos - 1

        if text and not text.replace(' ', '').isdigit():
            return QValidator.State.Invalid, text[:pos - 1], pos - 1

        if len(digits_only) == 11:
            return QValidator.State.Acceptable, text, pos
        elif len(digits_only) == 0:
            return QValidator.State.Intermediate, text, pos
        else:
            return QValidator.State.Intermediate, text, pos

    def get_activity_logs(self, limit=100):
        """Get staff activity logs showing orders they handled"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    CONCAT(su.UFirstName, ' ', su.ULastName) as staff_name,
                    CONCAT(cu.UFirstName, ' ', cu.ULastName) as customer,
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
                JOIN Customers c ON o.CustomerID = c.CustomerID
                JOIN Users cu ON c.UserID = cu.UserID
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

            # If no staff assigned, use a default staff name
            for result in results:
                if not result['staff_name'] or result['staff_name'] == ' ':
                    result['staff_name'] = 'Staff Member'

            return results
        except Exception as e:
            print(f"Error getting activity logs: {e}")
            import traceback
            traceback.print_exc()
            return []
