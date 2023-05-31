from django.forms import ModelForm
from . models import Article, Short, UsefulLink


class ArticleForm(ModelForm):

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

    class Meta:
        model = Short
        fields = ('header', 'published', 'body')
        labels = {
            "header": "Header",
            "published": "Published",
            "body": "Body (markdown)",
        }


class UsefulLinkForm(ModelForm):

    class Meta:
        model = UsefulLink
        fields = ('header', 'link', 'published', 'order')
        labels = {
            "header": "Header",
            "link": "Link",
            "published": "Published",
            "order": "Order",
        }
