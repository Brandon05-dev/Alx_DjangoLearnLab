import os
import sys
import django

# Absolute path to the project root (where manage.py lives)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Now Python can import myproject
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

django.setup()


from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)

# List all books in a library
def books_in_library(library_name):
    try:
        lib = Library.objects.get(name=library_name)
        return lib.books.all()
    except Library.DoesNotExist:
        return []

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    try:
        lib = Library.objects.get(name=library_name)
        return lib.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


if __name__ == "__main__":
    # Demo outputs
    print("Books by 'Jane Austen':")
    for book in books_by_author("Jane Austen"):
        print("-", book.title)

    print("\nBooks in 'Central Library':")
    for book in books_in_library("Central Library"):
        print("-", book.title)

    print("\nLibrarian for 'Central Library':")
    librarian = librarian_for_library("Central Library")
    if librarian:
        print(librarian.name)
    else:
        print("No librarian found")
