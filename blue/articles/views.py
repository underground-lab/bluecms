from django.shortcuts import render


def app_homepage(request):
    return render(request, 'homepage.html')


def app_page(request):
    return render(request, 'page.html')
