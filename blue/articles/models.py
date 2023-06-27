import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    header = models.CharField(_("Header"), max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(_("Published"), default=False)
    perex = models.TextField(_("Perex (markdown)"))
    body = models.TextField(_("Body (markdown)"))

    def __str__(self):
        return f"Article: {self.header}"

    @property
    def assets(self):
        return self.asset_set.all()
    
    class Meta:
        ordering = ['-id']



class Short(models.Model):
    header = models.CharField(_("Header"), max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(_("Published"), default=False)
    body = models.TextField(_("Body (markdown)"))

    def __str__(self):
        return f"Short: {self.header}"


class UsefulLink(models.Model):
    header = models.CharField(_("Header"), max_length=100)
    link = models.CharField(_("Link"), max_length=100)
    order = models.IntegerField(_("Order"))
    published = models.BooleanField(_("Published"), default=False)

    def __str__(self):
        return f"UsefulLink: {self.header}"


def article_directory_path(instance, filename):
    return 'assets/{0}/{1}'.format(instance.article.id, filename)


class Asset(models.Model):
    description = models.CharField(_("Description"), max_length=100)
    file = models.FileField(_("File"), upload_to=article_directory_path)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("Article"))
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asset: {self.description}"

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super(Asset, self).delete(*args, **kwargs)
