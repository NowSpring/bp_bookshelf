import uuid
from django.db import models
from django.conf import settings


class BookList(models.Model):

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(verbose_name = "タイトル", max_length = 100, default = "未登録")
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="所有者", related_name='owned_booklists')
  likes = models.ManyToManyField('members.Member', verbose_name="いいね", blank=True)
  order = models.IntegerField(verbose_name = "棚順")

  def __str__(self):

    return f"{self.title} by {self.owner}"


class Book(models.Model):

  id = models.CharField(max_length=500, primary_key=True)
  title = models.CharField(verbose_name="タイトル", max_length=100)
  description = models.CharField(verbose_name="概要", max_length=2000)
  price = models.IntegerField(verbose_name="価格", null=True, blank=True, default=None)
  link = models.CharField(verbose_name="商品リンク", max_length=500, null=True, blank=True, default=None)
  image = models.CharField(verbose_name="イメージ図", max_length=500, null=True, blank=True, default=None)

  class Meta:

    ordering = ['title']

  def __str__(self):

    return f"{self.title}"


class PersonalBook(models.Model):

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='personal_books')
  booklist = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name='personal_books')
  order = models.IntegerField(verbose_name="本順")

  class Meta:

    ordering = ['order']
    unique_together = ('book', 'booklist', 'order')

  def __str__(self):

    return f"{self.book.title} at {self.order} in {self.booklist.title}"
