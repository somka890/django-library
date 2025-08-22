from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Rating, UserProfile


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars"]
        widgets = {
            "stars": forms.RadioSelect(choices=Rating._meta.get_field("stars").choices)
        }



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Vartotojo vardas",
        help_text="Įveskite savo vartotojo vardą. Leidžiami tik raidės, skaičiai ir @/./+/-/_ simboliai."
    )
    first_name = forms.CharField(label="Vardas", required=True)
    last_name = forms.CharField(label="Pavardė", required=True)
    birth_year = forms.IntegerField(label="Gimimo metai", required=False)
    city = forms.CharField(label="Miestas", required=False)

    password1 = forms.CharField(
        label="Slaptažodis",
        widget=forms.PasswordInput,
        help_text="Slaptažodis turi būti bent 8 simbolių ilgio ir negali būti pernelyg paprastas."
    )
    password2 = forms.CharField(
        label="Slaptažodžio patvirtinimas",
        widget=forms.PasswordInput,
        help_text="Pakartokite tą patį slaptažodį dar kartą patvirtinimui."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "birth_year",
            "city",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                birth_year=self.cleaned_data.get("birth_year"),
                city=self.cleaned_data.get("city"),
            )
        return user
