from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_book(sender, **kwargs):
    from .models import Book
    if not Book.objects.filter(id="0123456789").exists():
        Book.objects.create(
            id="0123456789",
            title="未登録",
            description="未登録",
            price=None,
            link=None,
            image=None,
        )

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    def ready(self):

        import books.signals
        post_migrate.connect(create_default_book, sender=self)