from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian, UserProfile
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create sample data for the library system'

    def handle(self, *args, **options):
        # Create authors
        author1, _ = Author.objects.get_or_create(name="J.K. Rowling")
        author2, _ = Author.objects.get_or_create(name="George Orwell")
        author3, _ = Author.objects.get_or_create(name="Jane Austen")
        
        # Create books
        book1, _ = Book.objects.get_or_create(title="Harry Potter and the Philosopher's Stone", author=author1)
        book2, _ = Book.objects.get_or_create(title="1984", author=author2)
        book3, _ = Book.objects.get_or_create(title="Pride and Prejudice", author=author3)
        book4, _ = Book.objects.get_or_create(title="Animal Farm", author=author2)
        
        # Create library
        library, _ = Library.objects.get_or_create(name="Central Library")
        library.books.set([book1, book2, book3, book4])
        
        # Create librarian
        librarian, _ = Librarian.objects.get_or_create(name="John Smith", library=library)
        
        # Create test users with different roles
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={'email': 'admin@library.com', 'first_name': 'Admin', 'last_name': 'User'}
        )
        if created:
            admin_user.set_password('password123')
            admin_user.save()
        
        admin_profile, _ = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'Admin'}
        )
        
        # Create librarian user
        librarian_user, created = User.objects.get_or_create(
            username='librarian_user',
            defaults={'email': 'librarian@library.com', 'first_name': 'Librarian', 'last_name': 'User'}
        )
        if created:
            librarian_user.set_password('password123')
            librarian_user.save()
        
        librarian_profile, _ = UserProfile.objects.get_or_create(
            user=librarian_user,
            defaults={'role': 'Librarian'}
        )
        
        # Create member user
        member_user, created = User.objects.get_or_create(
            username='member_user',
            defaults={'email': 'member@library.com', 'first_name': 'Member', 'last_name': 'User'}
        )
        if created:
            member_user.set_password('password123')
            member_user.save()
        
        member_profile, _ = UserProfile.objects.get_or_create(
            user=member_user,
            defaults={'role': 'Member'}
        )
        
        # Grant permissions to admin and librarian
        content_type = ContentType.objects.get_for_model(Book)
        permissions = Permission.objects.filter(content_type=content_type)
        
        admin_user.user_permissions.set(permissions)
        librarian_user.user_permissions.set(permissions)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- Authors: {Author.objects.count()}\n'
                f'- Books: {Book.objects.count()}\n'
                f'- Libraries: {Library.objects.count()}\n'
                f'- Librarians: {Librarian.objects.count()}\n'
                f'- Users: admin_user, librarian_user, member_user (password: password123)\n'
            )
        )
