from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/support.html')

def cards(request):
    return render(request, 'core/cards.html')

def support(request):
    return render(request, 'core/support.html')

def investments(request):
    return render(request, 'core/investments.html')

def loans(request):
    return render(request, 'core/loans.html')   


def coming_soon(request):
    return render(request, "core/coming_soon.html")