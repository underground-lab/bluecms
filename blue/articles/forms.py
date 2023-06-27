from django.forms import ModelForm
from . models import Article, Short, UsefulLink, Asset


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ('header', 'perex', 'body', 'published')
        # labels = {
        #     "header": "Header",
        #     "published": "Published",
        #     "perex": "Perex (markdown)",
        #     "body": "Body (markdown)",
        # }


class ShortForm(ModelForm):

    class Meta:
        model = Short
        fields = ('header', 'body', 'published')


class UsefulLinkForm(ModelForm):

    class Meta:
        model = UsefulLink
        fields = ('header', 'link', 'order', 'published')


class AssetForm(ModelForm):

    class Meta:
        model = Asset
        fields = ('description', 'article', 'file')
