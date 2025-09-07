from relationship_app.models import Author, Book, Library, Librarian


def query_all_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None


def list_all_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None


def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Example usage:
if __name__ == "__main__":
    # Query all books by a specific author
    books_by_author = query_all_books_by_author("J.K. Rowling")
    if books_by_author:
        print(f"Books by J.K. Rowling: {[book.title for book in books_by_author]}")
    
    # List all books in a library
    books_in_library = list_all_books_in_library("Central Library")
    if books_in_library:
        print(f"Books in Central Library: {[book.title for book in books_in_library]}")
    
    # Retrieve librarian for a library
    librarian = retrieve_librarian_for_library("Central Library")
    if librarian:
        print(f"Librarian for Central Library: {librarian.name}")
