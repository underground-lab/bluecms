from django.forms import ModelForm
from . models import Article


class ArticelForm(ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
        labels = {
            "header": "Header",
            "author": "Author",
            "created_date": "Created",
            "published": "Published",
            "perex": "Perex (markdown)",
            "body": "Body (markdown)",
        }
