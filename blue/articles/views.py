from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Short, UsefulLink, Asset
from .forms import ArticleForm, ShortForm, UsefulLinkForm, AssetForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .utils import validate_email_address
from django.utils.translation import gettext as _


# Articles
##########

class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'homepage.html'
    ordering = ['-created_date']

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search_field')
        if search is None or len(search) < 3:
            messages.error(request, _("Search: Keyword '{}' is too short. Type at least 3 characters.").format(search))
            search = None
        if search is not None and len(search) > 100:
            messages.error(request, _("Search: Keyword is too long. Type maximum of 100 characters."))
            search = None
        self.object_list = self.get_queryset(search)
        context = self.get_context_data()
        if search is not None:
            context['search'] = search
        if search is not None:
            found = len(context['object_list'])
            messages.success(request, _("Searching for '{}': {} articles found.").format(search, found))
        return self.render_to_response(context)

    def get_queryset(self, search=None):
        queryset = super().get_queryset()
        if search == None:
            return queryset.filter(published=True)
        else:
            return queryset.filter(Q(published=True) & (Q(header__icontains=search) | Q(perex__icontains=search) | Q(body__icontains=search)))

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['shorts'] = Short.objects.filter(published=True).order_by('-created_date')
        context['useful_links'] = UsefulLink.objects.filter(published=True).order_by('order')
        context['menu'] = 1
        context['search'] = ''
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['menu'] = 1
        context['head'] = context['object'].header
        context['search'] = self.request.GET.get('search', '')
        if not self.request.user.is_active and not context['object'].published:
            raise Http404
        return context


# Redaction
###########


def redaction(request):
    context = {
        'menu': 2,
    }
    return render(request, 'redaction.html', context=context)


# Redaction - Article
#####################

class RedactionArticleListView(UserPassesTestMixin, ListView):
    model = Article
    paginate_by = 10
    template_name = 'redaction_article.html'
    ordering = ['-created_date']

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = '/redaction_article'

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False

class ShortDeleteView(UserPassesTestMixin, DeleteView):
    model = Short
    template_name = 'short_confirm_delete.html'
    success_url = '/redaction_short'

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

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

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class UsefulLinkDeleteView(UserPassesTestMixin, DeleteView):
    model = UsefulLink
    template_name = 'useful_link_confirm_delete.html'
    success_url = '/redaction_useful_link'

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


# Redaction - Asset
###################


class RedactionAssetListView(UserPassesTestMixin, ListView):
    model = Asset
    paginate_by = 10
    template_name = 'redaction_asset.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class AssetCreateView(UserPassesTestMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'asset_edit.html'
    success_url = "/redaction_asset"

    def get_context_data(self, *args, **kwargs):
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False


class AssetDeleteView(UserPassesTestMixin, DeleteView):
    model = Asset
    template_name = 'asset_confirm_delete.html'
    success_url = '/redaction_asset'

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)
        context['menu'] = 2
        return context

    def test_func(self):
        if self.request.user.is_active:
            return True
        else:
            return False

# Contact
#########


def contact(request):

    context = {
        'menu': 3,
    }

    if request.method == 'POST':
        your_name = request.POST.get('your_name')
        your_email = request.POST.get('your_email')
        your_enquiry = request.POST.get('your_enquiry')

        if settings.EMAIL_HOST == '':
            messages.error(request, _("Error: It seems E-Mail system is not configured yet."))
        elif not validate_email_address(your_email):
            messages.error(request, _("Error: {} seems not to be valid e-mail address.").format(your_email))
        else:
            recipientlist = [settings.EMAIL_RECIPIENT, ]
            send_mail(
                "BlueCms - Inquiry",
                f"Name: {your_name}\n E-Mail: {your_email}\n Text:\n {your_enquiry}",
                settings.EMAIL_HOST_USER,
                recipientlist
            )
            messages.success(request, _("Your inquiry has been sent."))

        return render(request, 'contact.html', context=context)
    else:
        return render(request, 'contact.html', context=context)
