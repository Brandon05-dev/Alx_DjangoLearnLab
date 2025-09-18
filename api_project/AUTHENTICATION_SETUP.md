# Django REST Framework Authentication and Permissions Setup

## Overview
This project implements token-based authentication using Django REST Framework's built-in authentication system.

## Authentication Configuration

### Settings (api_project/settings.py)
- Added 'rest_framework.authtoken' to INSTALLED_APPS
- Configured REST_FRAMEWORK settings with:
  - DEFAULT_AUTHENTICATION_CLASSES: TokenAuthentication
  - DEFAULT_PERMISSION_CLASSES: IsAuthenticated

### URL Configuration (api_project/urls.py)
- Added `/api-token-auth/` endpoint for token retrieval using `obtain_auth_token` view

### View Permissions (api/views.py)
- BookList and BookViewSet both require authentication via `permission_classes = [IsAuthenticated]`

## How Authentication Works

### 1. Obtaining a Token
Users can obtain an authentication token by sending a POST request to `/api-token-auth/` with their username and password:

```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{"token": "your_token_here"}
```

### 2. Using the Token
Include the token in the Authorization header for authenticated requests:

```bash
curl -H "Authorization: Token your_token_here" \
     http://127.0.0.1:8000/api/books_all/
```

### 3. API Endpoints with Authentication
All the following endpoints require authentication:

- GET `/api/books/` - List books (BookList view)
- GET `/api/books_all/` - List all books (BookViewSet)
- GET `/api/books_all/{id}/` - Retrieve specific book
- POST `/api/books_all/` - Create new book
- PUT `/api/books_all/{id}/` - Update book
- DELETE `/api/books_all/{id}/` - Delete book

### 4. Security Features
- Unauthenticated requests return HTTP 401 Unauthorized
- Each user gets a unique token for API access
- Token-based authentication is stateless and suitable for API consumption
- Tokens persist until manually revoked

## Testing Authentication
Run the authentication tests using the provided test script to verify:
- Unauthenticated access is properly blocked
- Token authentication endpoint works correctly
- Authenticated CRUD operations function as expected