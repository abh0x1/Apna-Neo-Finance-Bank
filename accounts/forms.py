from django import forms
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from .models import CustomUser

class AccountOpenForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username", "first_name", "last_name", "email", "city",
            "dob", "mobile", "address", "marital_status", "occupation",
            "account_plan", "account_type", "residency_status",
            "kyc_doc", "profile_image", "password1", "password2",
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),  # ✅ calendar picker
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "email",
            "mobile", "address", "profile_image",
            "upi_id",  
        ]
