from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticelForm
from django.contrib.auth.mixins import UserPassesTestMixin


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'homepage.html'
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'


def redaction(request):
    return render(request, 'redaction.html')


def contact(request):
    return render(request, 'contact.html')


class RedactionArticleListView(UserPassesTestMixin, ListView):
    model = Article
    paginate_by = 10
    template_name = 'redaction_article.html'
    ordering = ['-created_date']

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ArticleCreateView(UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticelForm
    template_name = 'article_edit.html'
    success_url = "/redaction_article"

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticelForm
    template_name = 'article_edit.html'
    success_url = "/redaction_article"

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = '/redaction_article'

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False
