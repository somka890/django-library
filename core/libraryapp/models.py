# ##### django models #####
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField("Vardas, pavardė", max_length=120)
    country = models.CharField("Šalis/Miestas", max_length=80, null=True, blank=True)
    birth_year = models.PositiveIntegerField("Gimimo metai", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField("Žanras", max_length=60, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Pavadinimas", max_length=200)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Autorius"
    )
    year = models.PositiveIntegerField("Išleidimo metai", null=True, blank=True)
    isbn = models.CharField("ISBN kodas", max_length=20, unique=True)
    genres = models.ManyToManyField(
        Genre, related_name="books", blank=True, verbose_name="Žanrai"
    )
    description = models.TextField("Aprašymas", blank=True, null=True)
    cover = models.ImageField("Viršelis", upload_to="covers/", blank=True, null=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"

    def __str__(self):
        return f"{self.title} ({self.author})"


class UserBookStatus(models.Model):
    STATUS_CHOICES = [
        ("read", "Perskaityta"),
        ("want", "Noriu perskaityti"),
        ("reading", "Skaitau dabar"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="book_statuses", verbose_name="Vartotojas"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="user_statuses", verbose_name="Knyga"
    )
    status = models.CharField("Statusas", max_length=20, choices=STATUS_CHOICES, default="read")
    created_at = models.DateTimeField("Sukurta", auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")
        verbose_name = "Knygos statusas"
        verbose_name_plural = "Knygų statusai"

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"


STAR_CHOICES = [(i, str(i)) for i in range(1, 6)]

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings", verbose_name="Knyga")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings", verbose_name="Vartotojas")
    stars = models.IntegerField("Įvertinimas (žvaigždutės)", choices=STAR_CHOICES)
    created_at = models.DateTimeField("Sukurta", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["book", "user"], name="unique_user_book_rating")
        ]
        ordering = ["-created_at"]
        verbose_name = "Įvertinimas"
        verbose_name_plural = "Įvertinimai"

    def __str__(self):
        return f"{self.book} - {self.user} [{self.stars}★]"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="Vartotojas"
    )
    birth_year = models.PositiveIntegerField("Gimimo metai", null=True, blank=True)
    city = models.CharField("Miestas", max_length=100, blank=True)

    class Meta:
        verbose_name = "Vartotojo profilis"
        verbose_name_plural = "Vartotojų profiliai"

    def __str__(self):
        return f"Profilis: {self.user.username}"
