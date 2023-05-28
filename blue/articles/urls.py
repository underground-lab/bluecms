from . import views
from django.urls import path


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='app_homepage'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='app_article'),
    #path('', views.app_homepage, name='app_homepage'),
    #path('page', views.app_page, name='app_page'),
]
