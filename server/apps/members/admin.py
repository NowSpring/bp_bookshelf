from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.utils.html import format_html
from django.urls import reverse

from members.models import Member
from books.models import BookList


class UserAdminConfig(UserAdmin):
    model = Member
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('username',)
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'birthday', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    change_form_template = 'admin/members/member/change_form.html'

admin.site.register(Member, UserAdminConfig)