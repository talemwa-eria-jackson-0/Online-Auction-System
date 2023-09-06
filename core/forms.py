from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["first_name"].widget.attrs.update({
    #         "class": "form-control",
    #         "placeholder": "Enter your first name",
    #     })

    #     self.fields["last_name"].widget.attrs.update({
    #         "class": "form-control",
    #         "placeholder": "Enter your last name",
    #     })

    #     self.fields["email"].widget.attrs.update({
    #         "class": "form-control",
    #         "placeholder": "Enter your Email",
    #     })

    #     self.fields["username"].widget.attrs.update({
    #         "class": "form-control",
    #         "placeholder": "Enter your username",
    #     })

    #     self.fields["password1"].widget.attrs.update({
    #         "class": "form-control",
    #         "placeholder": "Enter your password",
    #     })

        # self.fields["password2"].widget.attrs.update({
        #     "class": "form-control",
        #     "placeholder": "Confirm your password",
        # })

    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    username = forms.CharField(max_length=64)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
