# ##### django urls #####
from django.urls import path

# ##### django auth views #####
from django.contrib.auth import views as auth_views

# ##### project views #####
from .views import (
    BookListView,
    BookDetailView,
    RateBookView,
    register,
    profile,
    mark_as_read,
)

app_name = "libraryapp"

urlpatterns = [

    path("", BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/<int:pk>/rate/", RateBookView.as_view(), name="rate_book"),
    path("book/<int:pk>/mark_as_read/", mark_as_read, name="mark_as_read"),

    path("profile/", profile, name="profile"),

    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="libraryapp:book_list"), name="logout"),

    path("register/", register, name="register"),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="password_change.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),
]
