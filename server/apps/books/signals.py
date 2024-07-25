import os
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver, Signal
from django.conf import settings
from .models import BookList, Book, PersonalBook
from django.contrib.auth import get_user_model

User = get_user_model()
booklist_created = Signal()


@receiver(post_save, sender=User)
def create_user_booklist(sender, instance, created, **kwargs):

  if created:

    bookLists = []
    xBookList = BookList(owner = instance, order = 0)
    bookLists.append(xBookList)

    BookList.objects.bulk_create(bookLists)

    for booklist in bookLists:

      booklist_created.send(sender = BookList, instance = booklist)


@receiver(booklist_created)
def create_booklist_books(sender, instance, **kwargs):

  default_book = Book.objects.get(id="0123456789")

  # PersonalBookを作成してBookListに紐付け
  personal_books = []

  for i in range(5):

    personal_book = PersonalBook(book=default_book, booklist=instance, order=i)
    personal_books.append(personal_book)

  PersonalBook.objects.bulk_create(personal_books)

