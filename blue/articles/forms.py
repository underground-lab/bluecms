from django.forms import ModelForm
from . models import Article, Short, UsefulLink


class ArticleForm(ModelForm):

    template_name = "form_snippet.html"

    class Meta:
        model = Article
        fields = ('header', 'published', 'perex', 'body')
        labels = {
            "header": "Header",
            "published": "Published",
            "perex": "Perex (markdown)",
            "body": "Body (markdown)",
        }


class ShortForm(ModelForm):

    template_name = "form_snippet.html"

    class Meta:
        model = Short
        fields = ('header', 'published', 'body')
        labels = {
            "header": "Header",
            "published": "Published",
            "body": "Body (markdown)",
        }


class UsefulLinkForm(ModelForm):

    template_name = "form_snippet.html"

    class Meta:
        model = UsefulLink
        fields = ('header', 'link', 'published', 'order')
        labels = {
            "header": "Header",
            "link": "Link",
            "published": "Published",
            "order": "Order",
        }
