from django.db import transaction
from rest_framework import serializers

from members.serializers import MemberGetSerializer
from books.models import Book, BookList, PersonalBook

import logging

logger = logging.getLogger(__name__)


class PersonalBookSerializer(serializers.ModelSerializer):

  booklist_title = serializers.CharField(source='booklist.title', read_only=True)
  booklist_owner = serializers.CharField(source='booklist.owner.username', read_only=True)

  class Meta:

    model = PersonalBook
    fields = ['booklist_title', 'booklist_owner', 'order']


class BookSerializer(serializers.ModelSerializer):

  id = serializers.UUIDField(required=True)
  personal_books = PersonalBookSerializer(many=True, read_only=True)

  class Meta:

    model = Book
    fields = ['id', 'title', 'description', 'image', 'personal_books']


class BulkBookUpdateSerializer(serializers.Serializer):

    pass
#   books = BookSerializer(many=True)
#   id = serializers.UUIDField()

#   def update(self, instance, validated_data):

#     books_data = validated_data.pop('books')
#     id = validated_data.pop('id')
#     books_to_update = []

#     for book_data in books_data:

#       book = Book.objects.get(id=book_data['id'])
#       book.title = book_data['title']
#       book.description = book_data['description']
#       book.image = book_data['image']
#       book.order = book_data['order']
#       books_to_update.append(book)

#     with transaction.atomic():

#       Book.objects.bulk_update(books_to_update, ['title', 'description', 'image', 'order'])

#       booklist = BookList.objects.get(id = id)
#       booklist.save()

#     return books_to_update

class BookListSerializer(serializers.ModelSerializer):

  owner = MemberGetSerializer(read_only=True)
  books = BookSerializer(many=True, read_only=True, source='booklist')
  likes = serializers.SerializerMethodField()

  class Meta:

    model = BookList
    fields = "__all__"

  def get_books(self, obj):

    books = obj.booklist.order_by('order')

    return BookSerializer(books, many=True, read_only=True).data

  def get_likes(self, obj):

    request = self.context.get('request', None)
    reviewer_id = request.query_params.get('reviewer_id', None)
    mode = request.query_params.get('mode', 'edit')

    if mode == 'edit' or mode is None:

      return None  # likesフィールドを返さない

    elif mode == 'display':

      if reviewer_id:

        return str(reviewer_id) in [str(user.id) for user in obj.likes.all()]

    elif mode == 'admin':

      return MemberGetSerializer(obj.likes.all(), many=True).data

    return [user.username for user in obj.likes.all()]
