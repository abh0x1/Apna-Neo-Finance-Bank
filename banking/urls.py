from django.urls import path
from . import views
from accounts.views import user_update, change_password


app_name = "banking"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("netbanking/", views.netbanking, name="netbanking"),
    path("transaction-history/", views.transaction_history, name="transaction_history"),
    path("fund-transfer/", views.fund_transfer, name="fund_transfer"),
    path('virtual-card/', views.virtual_card_view, name='virtual_card'),
    path('branch-finder/', views.branch_finder, name='branch_finder'),
    path('net_coming_soon/', views.net_coming_soon, name='net_coming_soon'),
]
