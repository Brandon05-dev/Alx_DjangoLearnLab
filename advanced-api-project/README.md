# Advanced API Development with Django REST Framework

This project demonstrates advanced API development concepts using Django REST Framework, including custom serializers, views, filtering, searching, ordering, and comprehensive testing.

## Project Overview

The project implements a simple Book and Author management system with the following features:

- **Custom Models**: Author and Book models with one-to-many relationship
- **Custom Serializers**: BookSerializer with validation and AuthorSerializer with nested relationships
- **Generic Views**: Complete CRUD operations using DRF generic views
- **Advanced Querying**: Filtering, searching, and ordering capabilities
- **Authentication & Permissions**: Proper access control for different operations
- **Comprehensive Testing**: Unit tests covering all functionality

## Models

### Author
- `name`: String field for author's name
- **Relationship**: One-to-many with Book (an author can have multiple books)

### Book
- `title`: String field for book title
- `publication_year`: Integer field for publication year
- `author`: Foreign key to Author model
- **Validation**: Publication year cannot be in the future

## API Endpoints

### Book Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/api/books/` | List all books with filtering, searching, ordering | No |
| GET | `/api/books/<id>/` | Retrieve specific book | No |
| POST | `/api/books/create/` | Create new book | Yes |
| PUT | `/api/books/<id>/update/` | Update existing book | Yes |
| DELETE | `/api/books/<id>/delete/` | Delete book | Yes |

### Query Parameters

#### Filtering
- `?title=<title>` - Filter by book title
- `?author=<author_id>` - Filter by author ID
- `?publication_year=<year>` - Filter by publication year

#### Searching
- `?search=<query>` - Search in book title and author name

#### Ordering
- `?ordering=title` - Order by title (ascending)
- `?ordering=-title` - Order by title (descending)
- `?ordering=publication_year` - Order by publication year (ascending)
- `?ordering=-publication_year` - Order by publication year (descending)

## Installation and Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Testing

Run the comprehensive test suite:

```bash
python manage.py test api
```

The test suite includes:
- CRUD operation testing
- Authentication and permission testing
- Filtering, searching, and ordering functionality testing
- Data validation testing
- Error handling testing

## Example API Usage

### Create a Book (Authentication Required)
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "title": "Django for Beginners",
    "publication_year": 2023,
    "author": 1
  }'
```

### List Books with Filtering
```bash
# Get all books
curl http://localhost:8000/api/books/

# Filter by author
curl http://localhost:8000/api/books/?author=1

# Search by title
curl http://localhost:8000/api/books/?search=Django

# Order by publication year
curl http://localhost:8000/api/books/?ordering=-publication_year
```

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py          # Django settings with DRF configuration
│   ├── urls.py             # Main URL configuration
│   └── ...
├── api/
│   ├── models.py           # Author and Book models
│   ├── serializers.py      # Custom serializers with validation
│   ├── views.py            # Generic views with filtering/searching
│   ├── urls.py             # API endpoint routing
│   ├── test_views.py       # Comprehensive unit tests
│   └── ...
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Key Features Implemented

### Custom Serializers
- **BookSerializer**: Includes custom validation for publication year
- **AuthorSerializer**: Demonstrates nested serialization of related books

### Generic Views
- **ListView**: Read-only access to book collection
- **DetailView**: Read-only access to individual books
- **CreateView**: Authenticated book creation
- **UpdateView**: Authenticated book updates
- **DeleteView**: Authenticated book deletion

### Advanced Query Capabilities
- **Filtering**: Filter books by title, author, or publication year
- **Searching**: Full-text search across book titles and author names
- **Ordering**: Sort results by title or publication year

### Security & Permissions
- **Read Access**: Public access to list and detail views
- **Write Access**: Authenticated access required for create, update, delete
- **Data Validation**: Custom validation prevents invalid data entry

### Comprehensive Testing
14 test cases covering:
- All CRUD operations
- Authentication and permission enforcement
- Advanced query functionality
- Data validation
- Error handling

## Dependencies

- Django 5.2.6
- Django REST Framework 3.16.1
- django-filter 25.1

All dependencies are listed in `requirements.txt`.