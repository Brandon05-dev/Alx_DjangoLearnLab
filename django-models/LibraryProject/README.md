# LibraryProject

# Deep Dive into Django Models and Views

This project demonstrates advanced Django concepts including model relationships, views, URL configuration, user authentication, role-based access control, and custom permissions.

## Project Structure

```
LibraryProject/
├── LibraryProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── relationship_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   ├── query_samples.py
│   ├── management/
│   │   └── commands/
│   │       └── create_sample_data.py
│   ├── templates/
│   │   └── relationship_app/
│   │       ├── base.html
│   │       ├── list_books.html
│   │       ├── library_detail.html
│   │       ├── login.html
│   │       ├── logout.html
│   │       ├── register.html
│   │       ├── admin_view.html
│   │       ├── librarian_view.html
│   │       ├── member_view.html
│   │       ├── add_book.html
│   │       ├── edit_book.html
│   │       └── delete_book.html
│   └── migrations/
└── manage.py
```

## Features Implemented

### Task 0: Advanced Model Relationships

#### Models Created:
- **Author**: Stores author information with a name field
- **Book**: Stores book information with title and ForeignKey to Author
- **Library**: Stores library information with name and ManyToManyField to Books
- **Librarian**: Stores librarian information with name and OneToOneField to Library
- **UserProfile**: Extends Django User with role-based access (Admin, Librarian, Member)

#### Key Features:
- All models include `__str__` methods for better representation
- Custom permissions added to Book model for fine-grained access control
- Signal handlers for automatic UserProfile creation

#### Query Functions (query_samples.py):
- `query_all_books_by_author(author_name)`: Retrieves all books by a specific author
- `list_all_books_in_library(library_name)`: Lists all books in a library
- `retrieve_librarian_for_library(library_name)`: Gets the librarian for a library

### Task 1: Views and URL Configuration

#### Views Implemented:
- **Function-based view**: `list_books` - Lists all books with authors
- **Class-based view**: `LibraryDetailView` - Shows library details with books

#### URL Patterns:
- `/books/` - List all books
- `/library/<id>/` - Library detail view

### Task 2: User Authentication

#### Authentication Features:
- User registration with Django's built-in UserCreationForm
- Custom login and logout views
- Redirect configurations for authenticated users

#### Templates:
- `login.html` - User login form
- `logout.html` - Logout confirmation
- `register.html` - User registration form

### Task 3: Role-Based Access Control

#### User Roles:
- **Admin**: Full system access
- **Librarian**: Book management access
- **Member**: Read-only access

#### Role-based Views:
- `admin_view` - Admin dashboard (requires Admin role)
- `librarian_view` - Librarian dashboard (requires Librarian role)
- `member_view` - Member dashboard (requires Member role)

#### Features:
- Automatic UserProfile creation via Django signals
- Role-based navigation in templates
- User role checking with `@user_passes_test` decorator

### Task 4: Custom Permissions

#### Custom Permissions on Book Model:
- `can_add_book` - Permission to add new books
- `can_change_book` - Permission to edit existing books
- `can_delete_book` - Permission to delete books

#### Permission-secured Views:
- `add_book` - Add new books (requires `can_add_book` permission)
- `edit_book` - Edit existing books (requires `can_change_book` permission)
- `delete_book` - Delete books (requires `can_delete_book` permission)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django
```

### 2. Run Migrations
```bash
cd django-models/LibraryProject
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Sample Data
```bash
python manage.py create_sample_data
```

### 4. Run the Development Server
```bash
python manage.py runserver
```

## Test Users

The system comes with pre-created test users:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin_user | password123 | Admin | All book permissions |
| librarian_user | password123 | Librarian | All book permissions |
| member_user | password123 | Member | Read-only access |
| admin | admin123 | Django Superuser | All permissions |

## URL Endpoints

### Public Access:
- `/books/` - View all books
- `/login/` - User login
- `/register/` - User registration
- `/logout/` - User logout

### Role-based Access:
- `/admin/` - Admin panel (Admin role required)
- `/librarian/` - Librarian panel (Librarian role required)
- `/member/` - Member panel (Member role required)

### Permission-based Access:
- `/add_book/` - Add new book (can_add_book permission required)
- `/edit_book/<id>/` - Edit book (can_change_book permission required)
- `/delete_book/<id>/` - Delete book (can_delete_book permission required)

### Library Details:
- `/library/<id>/` - View library details and books

## Key Django Concepts Demonstrated

### 1. Model Relationships:
- **ForeignKey**: Book → Author (Many-to-One)
- **ManyToManyField**: Library ↔ Books (Many-to-Many)
- **OneToOneField**: Librarian → Library (One-to-One)
- **OneToOneField**: UserProfile → User (One-to-One)

### 2. Views:
- Function-based views with decorators
- Class-based views (DetailView)
- Authentication views (Login, Logout, Register)

### 3. Authentication & Authorization:
- Django's built-in authentication system
- Custom user profiles with role-based access
- Permission-based view protection
- Signal handlers for automatic profile creation

### 4. Templates:
- Template inheritance with base template
- Context variables and template tags
- Form handling in templates
- Conditional rendering based on user roles and permissions

### 5. URL Configuration:
- App-level URL patterns
- Project-level URL inclusion
- Named URL patterns for reverse lookups

### 6. Admin Interface:
- Custom admin classes for better model management
- List displays, filters, and search functionality

## Security Features

1. **CSRF Protection**: All forms include CSRF tokens
2. **Permission Checks**: Views protected with appropriate decorators
3. **Role-based Access**: Different dashboard views for different user roles
4. **Input Validation**: Form validation for user inputs
5. **Authentication Required**: Sensitive operations require login

## Testing the Application

1. **Register a new user** at `/register/`
2. **Login** with test credentials at `/login/`
3. **Browse books** at `/books/`
4. **Test role-based access** by visiting role-specific dashboards
5. **Try adding/editing/deleting books** (permissions required)
6. **Access Django admin** at `/admin/` with superuser credentials

## Advanced Features

- **Signal Handlers**: Automatic UserProfile creation
- **Custom Management Commands**: Sample data creation
- **Custom Permissions**: Fine-grained access control
- **Template Inheritance**: Consistent UI across all pages
- **Form Handling**: User registration and book management forms
- **Error Handling**: Graceful handling of permission denied scenarios

This project serves as a comprehensive example of Django's advanced features and best practices for building secure, role-based web applications.  
It serves as the base project setup with proper configuration of settings, manage.py, and apps.
