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
