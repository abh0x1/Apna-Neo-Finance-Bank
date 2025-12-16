from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # admin me kaunse fields show honge
    fieldsets = UserAdmin.fieldsets + (
        ("Banking Info", {
            "fields": (
                "dob", "mobile", "address",
                "account_plan", "account_type", "residency_status",
                "account_number", "virtual_card_number", "balance",
                "kyc_doc", "profile_image"
            )
        }),
    )

    # Signup me kaunse fields dikhaye
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Banking Info", {
            "fields": (
                "dob", "mobile", "address",
                "account_plan", "account_type", "residency_status",
                "kyc_doc", "profile_image"
            )
        }),
    )

    list_display = ("username", "email", "mobile", "account_number", "balance", "account_type", "account_plan")
    search_fields = ("username", "email", "mobile", "account_number")
    ordering = ("username",)

admin.site.register(CustomUser, CustomUserAdmin)
