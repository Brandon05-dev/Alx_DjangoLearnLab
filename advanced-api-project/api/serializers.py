from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization of Book model instances.
    
    This serializer includes custom validation to ensure the publication_year
    is not in the future, preventing invalid data entry.
    
    Fields:
    - All fields from the Book model (title, publication_year, author)
    
    Custom Validation:
    - publication_year: Cannot be greater than the current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation method to ensure publication_year is not in the future.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated publication_year value
            
        Raises:
            serializers.ValidationError: If publication_year is in the future
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization of Author model instances.
    
    This serializer includes nested BookSerializer to dynamically serialize
    all books related to each author, demonstrating the one-to-many relationship
    handling in Django REST Framework serializers.
    
    Fields:
    - name: The author's name
    - books: Nested serialization of all books written by this author
    
    Relationship Handling:
    - Uses the 'books' related_name from the Book model's foreign key
    - BookSerializer(many=True, read_only=True) creates a nested representation
    - read_only=True prevents creation/update of books through author endpoint
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']