from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article


# def app_homepage(request):
#     return render(request, 'homepage.html')


# def app_page(request):
#     return render(request, 'page.html')


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'homepage.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'page.html'
