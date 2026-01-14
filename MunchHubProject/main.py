import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from Database.DatabaseManager import DatabaseManager
from Main.LoginWindow import LoginWindow


def main():
    """Main entry point for the MunchHub application"""

    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("MunchHub")
    app.setOrganizationName("MunchHub")

    # Set application style
    app.setStyle('Fusion')

    # Initialize database manager with new database name
    db_manager = DatabaseManager(
        host='localhost',
        database='munchhubdb',  # Updated database name
        user='root',
        password=''  # Update with your MySQL password if needed
    )

    # Try to connect to database
    if not db_manager.connect():
        QMessageBox.critical(
            None,
            'Database Connection Error',
            'Failed to connect to the database.\n\n'
            'Please ensure:\n'
            '1. MySQL server is running\n'
            '2. Database "munchhubdb" exists\n'
            '3. Connection credentials are correct\n'
            '4. All required tables are created'
        )
        sys.exit(1)

    # Create and show login window
    login_window = LoginWindow(db_manager)
    login_window.show()

    # Start the event loop
    exit_code = app.exec()

    # Clean up database connection on exit
    db_manager.disconnect()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()