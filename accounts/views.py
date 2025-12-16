import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import CustomUser
from .forms import AccountOpenForm
from .forms import UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def open_account(request):
    if request.method == "POST":
        form = AccountOpenForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # save() will auto-generate IFSC & UPI
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("banking:dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountOpenForm()
    return render(request, "accounts/open_account.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user_obj = CustomUser.objects.get(username=username, mobile=phone)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name or user.username}!")
            return redirect("banking:dashboard")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")

@login_required
def user_logout(request):
    """Log the user out."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def dashboard(request):
    """Simple dashboard view (currently in accounts, should move to banking)."""
    user = request.user
    return render(request, "accounts/dashboard.html", {"user": user})


@login_required
def user_update(request):
    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            new_image = form.cleaned_data.get('profile_image')

            if new_image:
                # Delete all files in the user's profile_images folder
                folder_path = os.path.join(settings.MEDIA_ROOT, f"{user.username}_{user.mobile}", "profile_images")
                if os.path.isdir(folder_path):
                    for f in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, f)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                
                updated_user.profile_image = new_image

            updated_user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("banking:dashboard")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "accounts/user_update.html", {"form": form})

@login_required
def change_password(request):
    """Allow user to change password."""
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ✅ keeps user logged in
            messages.success(request, "Your password was changed successfully!")
            return redirect("banking:dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "accounts/change_password.html", {"form": form})