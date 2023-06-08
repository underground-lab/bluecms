from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    header = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    perex = models.TextField()
    body = models.TextField()

    def __str__(self):
        return f"Article: {self.header}"

    @property
    def assets(self):
        return self.asset_set.all()


class Short(models.Model):
    header = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    body = models.TextField()

    def __str__(self):
        return f"Short: {self.header}"


class UsefulLink(models.Model):
    header = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    order = models.IntegerField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"UsefulLink: {self.header}"


class Asset(models.Model):
    description = models.CharField(max_length=100)
    file = models.ImageField(upload_to='assets')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asset: {self.description}"
