from django.contrib import admin
from .models import Article, Short, UsefulLink, Asset

# Register your models here.

admin.site.register(Article)
admin.site.register(Short)
admin.site.register(UsefulLink)
admin.site.register(Asset)
