# Django Blog Application

A complete, fully functional blog application built with Django that includes user authentication, blog post management, commenting functionality, and advanced features like tagging and search.

## Features

### Core Features
- **User Authentication System**
  - User registration with email verification
  - Login/logout functionality
  - User profile management
  - Secure password handling with Django's built-in authentication

- **Blog Post Management (CRUD Operations)**
  - Create new blog posts
  - Read/view blog posts with pagination
  - Update existing posts (author only)
  - Delete posts (author only)
  - Rich text content support

- **Comment System**
  - Add comments to blog posts
  - Edit own comments
  - Delete own comments
  - Comment threading and timestamps

- **Advanced Features**
  - **Tagging System**: Tag posts with multiple keywords for better organization
  - **Search Functionality**: Search posts by title, content, or tags
  - **Tag-based Filtering**: View all posts with specific tags
  - **Responsive Design**: Mobile-friendly interface using Bootstrap

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_blog
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Blog: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
django_blog/
├── django_blog/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── blog/                        # Blog application
│   ├── models.py                # Post and Comment models
│   ├── views.py                 # All view logic
│   ├── forms.py                 # Forms for posts, comments, and user auth
│   ├── urls.py                  # Blog URL patterns
│   ├── admin.py                 # Admin interface configuration
│   └── migrations/              # Database migrations
├── templates/blog/              # HTML templates
│   ├── base.html                # Base template with navigation
│   ├── home.html                # Blog post listing
│   ├── post_detail.html         # Individual post view
│   ├── post_form.html           # Create/edit post form
│   ├── post_confirm_delete.html # Delete confirmation
│   ├── register.html            # User registration
│   ├── login.html               # User login
│   ├── logout.html              # Logout confirmation
│   ├── profile.html             # User profile management
│   ├── search_results.html      # Search results page
│   ├── posts_by_tag.html        # Tag-filtered posts
│   ├── update_comment.html      # Edit comment form
│   └── delete_comment.html      # Delete comment confirmation
├── static/blog/                 # Static files
│   └── main.css                 # Custom CSS styles
├── requirements.txt             # Python dependencies
└── manage.py                    # Django management script
```

## Usage Guide

### For Blog Visitors
1. **Browse Posts**: Visit the homepage to see all blog posts
2. **Read Posts**: Click on any post title to read the full content
3. **Search**: Use the search bar in the navigation to find specific posts
4. **Filter by Tags**: Click on any tag to see all posts with that tag
5. **Register**: Create an account to comment and create posts

### For Registered Users
1. **Create Posts**: Click "New Post" in the navigation
2. **Manage Posts**: Edit or delete your own posts from the post detail page
3. **Add Comments**: Leave comments on any blog post
4. **Manage Comments**: Edit or delete your own comments
5. **Update Profile**: Access your profile to update username and email
6. **Use Tags**: When creating posts, add tags separated by commas

### For Administrators
1. **Admin Interface**: Access `/admin/` to manage all content
2. **User Management**: Create, edit, and delete user accounts
3. **Content Moderation**: Manage posts and comments
4. **Tag Management**: Organize and clean up tags

## Models

### Post Model
- `title`: CharField (max 200 characters)
- `content`: TextField (unlimited text)
- `published_date`: DateTimeField (auto-set on creation)
- `author`: ForeignKey to User model
- `tags`: TaggableManager (from django-taggit)

### Comment Model
- `post`: ForeignKey to Post model
- `author`: ForeignKey to User model
- `content`: TextField
- `created_at`: DateTimeField (auto-set on creation)
- `updated_at`: DateTimeField (auto-updated on modification)

## URL Patterns

- `/` - Home page (post list)
- `/post/<id>/` - Post detail view
- `/post/new/` - Create new post
- `/post/<id>/update/` - Edit post
- `/post/<id>/delete/` - Delete post
- `/post/<id>/comment/` - Add comment
- `/comment/<id>/update/` - Edit comment
- `/comment/<id>/delete/` - Delete comment
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile
- `/search/` - Search posts
- `/tags/<tag_name>/` - Posts by tag

## Security Features

- CSRF protection on all forms
- User authentication required for creating content
- Authorization checks (users can only edit/delete their own content)
- Django's built-in password validation and hashing
- XSS protection through Django's template system

## Technologies Used

- **Django 5.2.6**: Web framework
- **django-taggit 6.1.0**: Tagging functionality
- **Bootstrap 5.1.3**: Frontend styling
- **SQLite**: Default database (easily configurable for PostgreSQL/MySQL)

## Testing

The application includes comprehensive testing for:
- User authentication flows
- CRUD operations for posts and comments
- Permission and authorization checks
- Search and tagging functionality

Run tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is built for educational purposes as part of the ALX Django Learning Lab.

## Support

For issues or questions, please check the documentation or create an issue in the repository.