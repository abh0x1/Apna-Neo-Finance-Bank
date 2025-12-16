from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("open-account/", views.open_account, name="open_account"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("update-profile/", views.user_update, name="user_update"),
    path("change-password/", views.change_password, name="change_password"),

]
