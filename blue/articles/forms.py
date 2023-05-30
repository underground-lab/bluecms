from django.forms import ModelForm
from . models import Article


class ArticelForm(ModelForm):

    class Meta:
        model = Article
        fields = ('header', 'published', 'perex', 'body')
        labels = {
            "header": "Header",
            "published": "Published",
            "perex": "Perex (markdown)",
            "body": "Body (markdown)",
        }
