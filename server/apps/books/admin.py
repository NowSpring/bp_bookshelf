from django.contrib import admin
from .models import BookList, Book, PersonalBook
from django.utils.html import format_html


@admin.register(BookList)
class BookListAdmin(admin.ModelAdmin):

  list_display = ('title', 'owner_name')
  filter_horizontal = ('likes',)
  change_form_template = 'admin/books/booklist/change_form.html'

  @admin.display(ordering='owner__username', description='編集者')
  def owner_name(self, obj):

    return obj.owner.username

  @admin.display(description='いいねしたユーザー')
  def like_names(self, obj):

    return ", ".join([like.username for like in obj.likes.all()])


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

  list_display = ('title', 'price')
  search_fields = ('title',)
  change_form_template = 'admin/books/book/change_form.html'

  def get_queryset(self, request):

    queryset = super().get_queryset(request)

    return queryset.prefetch_related('personal_books__booklist__owner')
