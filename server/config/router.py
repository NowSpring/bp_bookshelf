from rest_framework import routers

from apps.members.views import MemberViewSet
from apps.books.views import BookListViewSet, BookViewSet

router = routers.DefaultRouter()
router.register('member', MemberViewSet)
router.register('booklist', BookListViewSet)
router.register('book', BookViewSet)