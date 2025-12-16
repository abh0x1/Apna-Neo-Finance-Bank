from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cards/', views.cards, name='cards'),
    path('support/', views.contact, name='support'),
    path('investments/', views.investments, name='investments'),
    path('loans/', views.loans, name='loans'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    
]