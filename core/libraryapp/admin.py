from django.contrib import admin
from .models import Author, Genre, Book, Rating, UserBookStatus, UserProfile
from django.utils.html import format_html

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "birth_year")
    search_fields = ("name", "country")

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "isbn", "cover_preview")
    list_filter = ("author", "year", "genres")
    search_fields = ("title", "isbn")

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="height: 80px;"/>', obj.cover.url)
        return "—"
    cover_preview.short_description = "Viršelis"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "stars", "created_at")
    list_filter = ("stars", "created_at")
    search_fields = ("book__title", "user__username")

@admin.register(UserBookStatus)
class UserBookStatusAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "book__title")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birth_year", "city")
    search_fields = ("user__username", "city")
