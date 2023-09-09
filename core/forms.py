# from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            # "placeholder": "Enter your email"
        })


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



class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'description', 'start_price', 'end_time', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class":"form-control",
            "id": "name",
        })

        self.fields["start_price"].widget.attrs.update({
            "class":"form-control",
            "id": "start_price"
        })

        self.fields["end_time"].widget.attrs.update({
            "class":"form-control",
            "id": "end_time"
        })

        self.fields["image"].widget.attrs.update({
            "class":"form-control",
            "id": "image"
        })

        self.fields["description"].widget.attrs.update({
            "class":"form-control",
            "id": "description"
        })


# class BidForm(forms.Form):
#     bid_amount = forms.DecimalField(
#         label='Bid Amount',
#         min_value=0.01,  # Minimum bid amount
#         required=True,
#         widget=forms.NumberInput(attrs={'step': '0.01'}),  # Optional: Specify the input step
#     )

class BidForm(ModelForm):
    class Meta:
        model = models.Bid
        fields = ["bid_price"]
