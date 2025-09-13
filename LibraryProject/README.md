# LibraryProject

This is a Django project for managing a library system. It includes features for managing books, authors, and other library resources.

## Project Structure

- `LibraryProject/` - Main Django project directory
- `bookshelf/` - Django app for library management
- `manage.py` - Django management script
- `db.sqlite3` - SQLite database file

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Features
- Book and author management
- Admin interface
- User authentication (if enabled)

## License
This project is for educational purposes.
