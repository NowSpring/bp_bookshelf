import uuid
from django.db import models
from django.conf import settings
from django.contrib.admin.models import LogEntry, CHANGE
from django.utils.translation import gettext_lazy as _


class BookList(models.Model):

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(verbose_name = "タイトル", max_length = 100, default = "未登録")
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="所有者", related_name='owned_booklists')
  likes = models.ManyToManyField('members.Member', verbose_name="いいね", blank=True)
  order = models.PositiveIntegerField(verbose_name = "棚順")
  version = models.PositiveBigIntegerField(default = 0)

  def __str__(self):

    return f"{self.title} by {self.owner}"

  def save(self, *args, **kwargs):
    # 変更履歴のカウントに基づいてversionを更新

    if self.pk:

      self.version = LogEntry.objects.filter(
        content_type__model='booklist',
        object_id=self.pk,
        action_flag=CHANGE
      ).count()

    super().save(*args, **kwargs)

  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)
    # 新規作成時にversionを初期化

    if not self.pk:

      self.version = 0

    else:

      self.version = LogEntry.objects.filter(
        content_type__model='booklist',
        object_id=self.pk,
        action_flag=CHANGE
      ).count()


class Book(models.Model):

  id = models.CharField(max_length=500, primary_key=True)
  title = models.CharField(verbose_name="タイトル", max_length=100)
  description = models.CharField(verbose_name="概要", max_length=2000)
  price = models.PositiveIntegerField(verbose_name="価格", null=True, blank=True, default=None)
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
  order = models.PositiveIntegerField(verbose_name="本順")

  class Meta:

    ordering = ['order']
    unique_together = ('book', 'booklist', 'order')


class BookListLike(models.Model):

  reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_booklist_likes')
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booklist_likes')
  booklists = models.JSONField(default=list)

  class Meta:

    unique_together = ('reviewer', 'owner')

  def __str__(self):

    return f"{self.reviewer} liked booklists of {self.owner}"