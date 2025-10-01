from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model represents authors who can write multiple books.
    This model establishes the 'one' side of the one-to-many relationship with Book.
    
    Fields:
    - name: String field to store the author's full name
    """
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents individual books in the system.
    Each book is associated with one author through a foreign key relationship.
    This model establishes the 'many' side of the one-to-many relationship with Author.
    
    Fields:
    - title: String field for the book's title
    - publication_year: Integer field for the year the book was published
    - author: Foreign key linking to the Author model (one-to-many relationship)
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
