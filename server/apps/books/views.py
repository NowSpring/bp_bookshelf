from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action

from members.models import Member
from books.models import BookList, Book, PersonalBook
from books.serializers import BookListSerializer, BookSerializer, BulkBookUpdateSerializer, PersonalBookSerializer

class BookListViewSet(viewsets.ModelViewSet):

  queryset = BookList.objects.all()
  serializer_class = BookListSerializer

  def get_queryset(self):

    queryset = super().get_queryset().select_related('owner').prefetch_related('booklist')
    member_id = self.request.query_params.get('member_id', None)

    if member_id is not None:

      queryset = queryset.filter(owner__id=member_id)

    queryset = queryset.order_by('owner__username')

    return queryset

  # ↓お気に入りだけGETするよう改変
  # @action(detail=False, methods=['get'], url_path='admin_view')
  # def admin_view(self, request):

  #   booklisttype_id = request.query_params.get('booklisttype_id', None)

  #   booklists = BookList.objects.filter(type__id=booklisttype_id).select_related('owner').prefetch_related('likes', 'booklist').order_by('owner__username')
  #   response_data = []

  #   for booklist in booklists:

  #     owner = booklist.owner
  #     books = booklist.booklist.all()
  #     likes = booklist.likes.all()

  #     book_data = {
  #       'id': booklist.id,
  #       'books': [
  #           {
  #               'id': book.id,
  #               'title': book.title,
  #               'order': book.order
  #           } for book in books
  #       ],
  #       'like_by': [
  #           {
  #               'id': like.id,
  #               'name': like.username
  #           } for like in likes
  #       ]
  #     }

  #     owner_data = {
  #       'id': owner.id,
  #       'name': owner.username
  #     }

  #     like_booklists = [
  #       str(liked_booklist.id) for liked_booklist in owner.liked_booklists.filter(type__id=booklisttype_id)
  #     ]

  #     response_data.append({
  #       'owner': owner_data,
  #       'booklist': book_data,
  #       'like_booklist': like_booklists
  #     })

  #   return Response(response_data, status=status.HTTP_200_OK)

  @action(detail=False, methods=['post'], url_path='like')
  def like(self, request):

    booklist_id = request.data.get('booklist_id')
    reviewer_id = request.data.get('reviewer_id')
    like = request.data.get('like')

    try:

      booklist = BookList.objects.get(id=booklist_id)
      reviewer = Member.objects.get(id=reviewer_id)

      if like:

        if not booklist.likes.filter(id=reviewer_id).exists():

          booklist.likes.add(reviewer)

      else:

        if booklist.likes.filter(id=reviewer_id).exists():

          booklist.likes.remove(reviewer)

      booklist.save()

      return Response(status=status.HTTP_204_NO_CONTENT)

    except BookList.DoesNotExist:

      return Response({'error': 'BookList not found'}, status=status.HTTP_404_NOT_FOUND)

    except Member.DoesNotExist:

      return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

      return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ModelViewSet):

  queryset = Book.objects.all()
  serializer_class = BookSerializer

  def get_queryset(self):

    queryset = super().get_queryset().prefetch_related('personal_books__booklist__owner')
    booklist_id = self.request.query_params.get('booklist_id', None)

    if booklist_id is not None:

      queryset = queryset.filter(personal_books__booklist=booklist_id)

    return queryset

  @action(detail=False, methods=['get'], url_path='personalbook')
  def get_personalbook(self, request, *args, **kwargs):
    personalbook_id = request.query_params.get('id')

    if not personalbook_id:

      return Response({"detail": "PersonalBook ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:

      personalbook = PersonalBook.objects.select_related('book', 'booklist__owner').get(id=personalbook_id)

    except PersonalBook.DoesNotExist:

      return Response({"detail": "PersonalBook not found."}, status=status.HTTP_404_NOT_FOUND)

    book_serializer = BookSerializer(personalbook.book)
    personalbook_serializer = PersonalBookSerializer(personalbook)

    response_data = {
      'personalbook': personalbook_serializer.data,
      'book': book_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)

  @action(detail=False, methods=['get'], url_path='book')
  def get_book(self, request, *args, **kwargs):

    book_id = request.query_params.get('id')

    if not book_id:

      return Response({"detail": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:

      book = Book.objects.prefetch_related('personal_books__booklist__owner').get(id=book_id)

    except Book.DoesNotExist:

      return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    book_serializer = BookSerializer(book)
    personalbooks = book.personal_books.all()
    personalbook_serializer = PersonalBookSerializer(personalbooks, many=True)

    response_data = {
      'book': book_serializer.data,
      'personal_books': personalbook_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)
