from . import views
from django.urls import path


urlpatterns = [
    path('', views.app_homepage, name='app_homepage'),
    path('page', views.app_page, name='app_page'),
]
