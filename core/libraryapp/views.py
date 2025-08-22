# ##### django shortcuts #####
from django.shortcuts import render, redirect, get_object_or_404

# ##### django urls and views #####
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView

# ##### django auth #####
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# ##### django orm #####
from django.db.models import Avg

# ##### project models #####
from .models import Book, Author, Genre, Rating, UserBookStatus

# ##### project forms #####
from .forms import RatingForm, CustomUserCreationForm


# ##### book list #####
class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = 4

    def get_queryset(self):
        books = Book.objects.all().annotate(avg_rating=Avg("ratings__stars"))

        # search params
        title = self.request.GET.get("title")
        author = self.request.GET.get("author")
        genre = self.request.GET.get("genre")
        year_from = self.request.GET.get("year_from")
        year_to = self.request.GET.get("year_to")
        order = self.request.GET.get("order", "title")

        if title:
            books = books.filter(title__icontains=title)

        if author:
            books = books.filter(author__name__icontains=author)

        if genre:
            books = books.filter(genres__id=genre)

        if year_from:
            books = books.filter(year__gte=year_from)

        if year_to:
            books = books.filter(year__lte=year_to)

        if order not in ["title", "year"]:
            order = "title"

        return books.order_by(order, "title").distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.all()
        context["genres"] = Genre.objects.all()
        context["current"] = {
            "title": self.request.GET.get("title", ""),
            "author": self.request.GET.get("author", ""),
            "genre": self.request.GET.get("genre", ""),
            "year_from": self.request.GET.get("year_from", ""),
            "year_to": self.request.GET.get("year_to", ""),
            "order": self.request.GET.get("order", "title"),
        }
        return context


# ##### book detail #####
class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"
    paginate_by = 4

    def get_queryset(self):
        return Book.objects.all().annotate(avg_rating=Avg("ratings__stars"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        rating = None
        has_read = False

        if user.is_authenticated:
            rating = Rating.objects.filter(book=self.object, user=user).first()
            has_read = UserBookStatus.objects.filter(
                user=user,
                book=self.object,
                status="read"
            ).exists()

        context["form"] = RatingForm(initial={"stars": getattr(rating, "stars", None)})
        context["user_rating"] = rating
        context["has_read"] = has_read
        return context


# ##### mark as read #####
@login_required
def mark_as_read(request, pk):
    book = get_object_or_404(Book, pk=pk)

    status, created = UserBookStatus.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={"status": "read"}
    )

    if not created and status.status != "read":
        status.status = "read"
        status.save()

    messages.success(request, f"Knyga „{book.title}“ pažymėta kaip perskaityta.")
    return redirect("libraryapp:book_detail", pk=book.pk)


# ##### rate book #####
class RateBookView(LoginRequiredMixin, FormView):
    form_class = RatingForm
    template_name = "book_detail.html"

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])

        # only if book is marked as read
        if not UserBookStatus.objects.filter(
                user=self.request.user,
                book=book,
                status="read"
        ).exists():
            messages.error(
                self.request,
                "Norėdami įvertinti, pirmiausia pažymėkite knygą kaip perskaitytą."
            )
            return redirect(reverse("libraryapp:book_detail", kwargs={"pk": book.pk}))

        rating, created = Rating.objects.update_or_create(
            book=book,
            user=self.request.user,
            defaults={"stars": form.cleaned_data["stars"]}
        )

        if created:
            messages.success(self.request, "Ačiū! Jūsų įvertinimas išsaugotas.")
        else:
            messages.success(self.request, "Jūsų įvertinimas atnaujintas.")

        return redirect(reverse("libraryapp:book_detail", kwargs={"pk": book.pk}))

    def form_invalid(self, form):
        messages.error(self.request, "Nepavyko išsaugoti įvertinimo. Patikrinkite formą.")
        return redirect(reverse("libraryapp:book_detail", kwargs={"pk": self.kwargs["pk"]}))


# ##### register #####
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("libraryapp:book_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


# ##### profile #####
@login_required
def profile(request):
    # filter by book status
    filter_status = request.GET.get("status", "read")

    books_status = UserBookStatus.objects.filter(
        user=request.user,
        status=filter_status
    ).select_related("book")

    read_count = UserBookStatus.objects.filter(user=request.user, status="read").count()
    rated_count = Rating.objects.filter(user=request.user).count()

    return render(request, "profile.html", {
        "filter_status": filter_status,
        "books_status": books_status,
        "read_count": read_count,
        "rated_count": rated_count,
    })
