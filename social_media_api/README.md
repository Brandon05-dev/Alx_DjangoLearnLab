# Social Media API

A complete Django REST Framework project implementing a social media platform with user authentication, posts, comments, likes, following system, and notifications.

## 🚀 Features

### Task 0 - User Authentication
- ✅ Custom User model with bio, profile picture, and followers
- ✅ User registration with automatic token generation
- ✅ User login with token authentication
- ✅ User profile management
- ✅ Token-based authentication using Django REST Framework

### Task 1 - Posts & Comments
- ✅ CRUD operations for posts (content + optional image)
- ✅ CRUD operations for comments on posts
- ✅ Permission system: only authors can edit/delete their content
- ✅ Post filtering and search functionality
- ✅ Image upload support for posts

### Task 2 - Follow System & Feed
- ✅ Follow/unfollow other users
- ✅ Personal feed showing posts from followed users
- ✅ User discovery endpoint

### Task 3 - Likes & Notifications
- ✅ Like/unlike posts functionality
- ✅ Automatic notifications for:
  - New followers
  - Post likes
  - Post comments
- ✅ Mark notifications as read/unread
- ✅ Unread notifications counter

### Task 4 - Deployment Setup
- ✅ Environment configuration with .env support
- ✅ Production-ready settings
- ✅ Static files configuration with WhiteNoise
- ✅ CORS configuration
- ✅ PostgreSQL support for production

## 🏗️ Project Structure

```
Alx_DjangoLearnLab/
└── social_media_api/
    ├── accounts/           # User authentication & profile management
    ├── posts/              # Posts, comments, likes, and feed
    ├── notifications/      # Notification system
    ├── social_media_api/   # Django project settings
    ├── .env               # Environment variables
    ├── requirements.txt   # Python dependencies
    └── manage.py         # Django management script
```

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
cd Alx_DjangoLearnLab/social_media_api
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file with:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=  # Optional: PostgreSQL URL for production
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Authentication Endpoints
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/profile/` - Get/Update user profile
- `GET /api/accounts/users/` - List all users

### Follow System
- `POST /api/accounts/<username>/follow/` - Follow/unfollow user
  ```json
  {"action": "follow"}  // or "unfollow"
  ```

### Posts Endpoints
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/<id>/` - Get specific post
- `PUT /api/posts/<id>/` - Update post (author only)
- `DELETE /api/posts/<id>/` - Delete post (author only)
- `POST /api/posts/<id>/like/` - Like/unlike post

### Comments Endpoints
- `GET /api/posts/<post_id>/comments/` - List post comments
- `POST /api/posts/<post_id>/comments/` - Create comment
- `GET /api/posts/comments/<id>/` - Get specific comment
- `PUT /api/posts/comments/<id>/` - Update comment (author only)
- `DELETE /api/posts/comments/<id>/` - Delete comment (author only)

### Feed & Notifications
- `GET /api/posts/feed/` - Get personalized feed
- `GET /api/notifications/` - List user notifications
- `PATCH /api/notifications/<id>/read/` - Mark notification as read
- `PATCH /api/notifications/mark-all-read/` - Mark all notifications as read
- `GET /api/notifications/unread-count/` - Get unread notifications count

## 🔐 Authentication

All API endpoints (except registration and login) require authentication using Token-based authentication.

### Headers Required:
```
Authorization: Token your-token-here
Content-Type: application/json
```

### Example Usage:

#### 1. Register User
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

#### 3. Create Post
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{
    "content": "Hello, Social Media API!"
  }'
```

#### 4. Follow User
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/testuser2/follow/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{
    "action": "follow"
  }'
```

## 🚀 Deployment

### Production Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### For Render.com Deployment
1. Set environment variables in Render dashboard
2. Use the provided `requirements.txt`
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn social_media_api.wsgi:application`

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📝 Models Overview

### User Model (accounts/models.py)
- Extends Django's AbstractUser
- Additional fields: bio, profile_picture, followers (ManyToMany)

### Post Model (posts/models.py)
- Fields: author, content, image, created_at, updated_at
- Related: comments, likes

### Comment Model (posts/models.py)
- Fields: post, author, text, created_at, updated_at

### Like Model (posts/models.py)
- Fields: user, post, created_at
- Unique constraint on (user, post)

### Notification Model (notifications/models.py)
- Fields: recipient, actor, verb, target (generic foreign key), timestamp, read
- Supports notifications for follows, likes, and comments

## 👨‍💻 Development

### Key Features Implemented:
- Custom user model with social features
- Token-based authentication
- RESTful API design
- Permission-based access control
- Generic foreign keys for flexible notifications
- Optimized database queries with select_related and prefetch_related
- Image upload handling
- CORS support for frontend integration
- Environment-based configuration

### Django Packages Used:
- Django REST Framework
- Django Filter
- Django CORS Headers
- Pillow (image processing)
- WhiteNoise (static files)
- python-dotenv (environment variables)

## 📄 License

This project is part of the ALX DjangoLearnLab curriculum.

## 🤝 Contributing

This is an educational project. Feel free to fork and experiment!