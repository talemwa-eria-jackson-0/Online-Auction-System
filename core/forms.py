# from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
        })

        # Removing validation texts from the register form
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""



