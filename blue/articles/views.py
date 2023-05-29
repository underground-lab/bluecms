from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticelForm


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'homepage.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'


def redaction(request):
    return render(request, 'redaction.html')


class RedactionArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'redaction_article.html'


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticelForm
    template_name = 'article_edit.html'
    success_url = "/redaction_article"


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticelForm
    template_name = 'article_edit.html'
    success_url = "/redaction_article"


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = '/redaction_article'
