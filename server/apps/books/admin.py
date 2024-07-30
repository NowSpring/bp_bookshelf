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

  def get_queryset(self, request):

    queryset = super().get_queryset(request).select_related('owner').prefetch_related('personal_books__book')

    return queryset

  def change_view(self, request, object_id, form_url='', extra_context=None):

    extra_context = extra_context or {}
    extra_context['show_table'] = True  # 変更画面ではテーブルを表示

    return super().change_view(request, object_id, form_url, extra_context=extra_context)

  def add_view(self, request, form_url='', extra_context=None):

    extra_context = extra_context or {}
    extra_context['show_table'] = False  # 追加画面ではテーブルを表示しない

    return super().add_view(request, form_url, extra_context=extra_context)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

  list_display = ('title', 'price')
  search_fields = ('title',)
  change_form_template = 'admin/books/book/change_form.html'

  def get_queryset(self, request):

    queryset = super().get_queryset(request)

    return queryset.prefetch_related('personal_books__booklist__owner')

  def change_view(self, request, object_id, form_url='', extra_context=None):

    extra_context = extra_context or {}
    extra_context['show_table'] = True  # 変更画面ではテーブルを表示

    return super().change_view(request, object_id, form_url, extra_context=extra_context)

  def add_view(self, request, form_url='', extra_context=None):

    extra_context = extra_context or {}
    extra_context['show_table'] = False  # 追加画面ではテーブルを表示しない

    return super().add_view(request, form_url, extra_context=extra_context)