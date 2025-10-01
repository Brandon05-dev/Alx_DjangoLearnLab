from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Comprehensive unit tests for the Book API endpoints.
    
    This test class covers all CRUD operations, authentication, permissions,
    and advanced query capabilities (filtering, searching, ordering) for the Book API.
    """
    
    def setUp(self):
        """
        Set up test data that will be used across multiple test methods.
        Creates test users, authors, and books for testing various scenarios.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='Test Author 1')
        self.author2 = Author.objects.create(name='Test Author 2')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Another Book',
            publication_year=2021,
            author=self.author2
        )
        
        # Define API endpoints
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})
    
    def test_get_book_list(self):
        """
        Test retrieving the list of all books.
        Should return 200 status and correct book data for unauthenticated users.
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Another Book')  # Default ordering by title
        self.assertEqual(response.data[1]['title'], 'Test Book 1')
    
    def test_get_book_detail(self):
        """
        Test retrieving a single book by ID.
        Should return 200 status and correct book data for unauthenticated users.
        """
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['author'], self.author1.pk)
    
    def test_create_book_authenticated(self):
        """
        Test creating a new book with authenticated user.
        Should return 201 status and create the book successfully.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication.
        Should return 403 status and not create the book.
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # No new book created
    
    def test_update_book_authenticated(self):
        """
        Test updating an existing book with authenticated user.
        Should return 200 status and update the book successfully.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Test Book',
            'publication_year': 2022,
            'author': self.author2.pk
        }
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the book was updated
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Test Book')
        self.assertEqual(updated_book.publication_year, 2022)
        self.assertEqual(updated_book.author, self.author2)
    
    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        Should return 403 status and not update the book.
        """
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 2022,
            'author': self.author2.pk
        }
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the book was not updated
        book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(book.title, 'Test Book 1')  # Original title unchanged
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authenticated user.
        Should return 204 status and delete the book successfully.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # One book remaining
    
    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        Should return 403 status and not delete the book.
        """
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # Both books still exist
    
    def test_book_filtering(self):
        """
        Test filtering functionality on the book list endpoint.
        Should return filtered results based on query parameters.
        """
        # Test filtering by author
        response = self.client.get(self.book_list_url, {'author': self.author1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        
        # Test filtering by publication year
        response = self.client.get(self.book_list_url, {'publication_year': 2021})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Another Book')
    
    def test_book_searching(self):
        """
        Test search functionality on the book list endpoint.
        Should return books matching the search query in title or author name.
        """
        # Test searching by book title
        response = self.client.get(self.book_list_url, {'search': 'Another'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Another Book')
        
        # Test searching by author name
        response = self.client.get(self.book_list_url, {'search': 'Author 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
    
    def test_book_ordering(self):
        """
        Test ordering functionality on the book list endpoint.
        Should return books ordered by the specified field.
        """
        # Test ordering by publication year (ascending)
        response = self.client.get(self.book_list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020)
        self.assertEqual(response.data[1]['publication_year'], 2021)
        
        # Test ordering by publication year (descending)
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)
        self.assertEqual(response.data[1]['publication_year'], 2020)
    
    def test_book_validation(self):
        """
        Test custom validation in BookSerializer.
        Should reject books with publication_year in the future.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertEqual(Book.objects.count(), 2)  # No new book created
    
    def test_nonexistent_book_detail(self):
        """
        Test retrieving a non-existent book.
        Should return 404 status.
        """
        nonexistent_url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_invalid_book_data(self):
        """
        Test creating a book with invalid data.
        Should return 400 status with validation errors.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': '',  # Empty title
            'publication_year': 'invalid',  # Invalid year format
            'author': 9999  # Non-existent author
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 2)  # No new book created