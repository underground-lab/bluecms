from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Short, UsefulLink
from .forms import ArticleForm, ShortForm, UsefulLinkForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Articles
##########

class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'homepage.html'
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['shorts'] = Short.objects.filter(published=True).order_by('-created_date')
        context['useful_links'] = UsefulLink.objects.filter(published=True).order_by('order')
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        if not self.request.user.is_active and not context['object'].published:
            raise Http404
        return context


# Redaction
###########


def redaction(request):
    return render(request, 'redaction.html')


# Redaction - Article
#####################

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
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = "/redaction_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
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


# Redaction - Short
###################


class RedactionShortListView(UserPassesTestMixin, ListView):
    model = Short
    paginate_by = 10
    template_name = 'redaction_short.html'
    ordering = ['-created_date']

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ShortCreateView(UserPassesTestMixin, CreateView):
    model = Short
    form_class = ShortForm
    template_name = 'short_edit.html'
    success_url = "/redaction_short"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ShortCreateView, self).form_valid(form)

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ShortUpdateView(UserPassesTestMixin, UpdateView):
    model = Short
    form_class = ShortForm
    template_name = 'short_edit.html'
    success_url = "/redaction_short"

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False

class ShortDeleteView(UserPassesTestMixin, DeleteView):
    model = Short
    template_name = 'short_confirm_delete.html'
    success_url = '/redaction_short'

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


# Redaction - UsefulLink
########################


class RedactionUsefulLinkListView(UserPassesTestMixin, ListView):
    model = UsefulLink
    paginate_by = 10
    template_name = 'redaction_useful_link.html'
    ordering = ['order']

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class UsefulLinkCreateView(UserPassesTestMixin, CreateView):
    model = UsefulLink
    form_class = UsefulLinkForm
    template_name = 'useful_link_edit.html'
    success_url = "/redaction_useful_link"

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class UsefulLinkUpdateView(UserPassesTestMixin, UpdateView):
    model = UsefulLink
    form_class = UsefulLinkForm
    template_name = 'useful_link_edit.html'
    success_url = "/redaction_useful_link"

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class UsefulLinkDeleteView(UserPassesTestMixin, DeleteView):
    model = UsefulLink
    template_name = 'useful_link_confirm_delete.html'
    success_url = '/redaction_useful_link'

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


# Contact
#########


def contact(request):
    if request.method == 'POST':
        your_name = request.POST.get('your_name')
        your_email = request.POST.get('your_email')
        your_enquiry = request.POST.get('your_enquiry')

        recipientlist = [settings.EMAIL_RECIPIENT, ]
        send_mail(
            "BlueCms - Inquiry",
            f"Name: {your_name}\n E-Mail: {your_email}\n Text:\n {your_enquiry}",
            settings.EMAIL_HOST_USER,
            recipientlist
        )

        messages.success(request, "Your inquiry has been sent.")
        return render(request, 'contact.html')
    else:
        return render(request, 'contact.html')
