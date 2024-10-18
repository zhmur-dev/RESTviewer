from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    CustomUser,
    Genre,
    Review,
    Title
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
        'date_joined',
        'role',
        'confirmation_code',
    )
    list_editable = (
        'email',
        'is_staff',
        'role',
        'confirmation_code',
    )
    list_filter = ('role',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'description', 'category']
    search_fields = ['name', 'year', 'description', 'genre']
    list_filter = ['category', 'genre', 'year']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'pub_date', 'author', 'title', 'score', 'text']
    search_fields = ['text']
    list_filter = ['pub_date', 'author', 'title', 'score']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'pub_date', 'author', 'review', 'text']
    search_fields = ['text']
    list_filter = ['pub_date', 'author', 'review']
