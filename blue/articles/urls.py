from . import views
from django.urls import path


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='homepage'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article'),
    path('redaction', views.redaction, name='redaction'),
    path('redaction_article', views.RedactionArticleListView.as_view(), name='redaction_article'),
    path('article_create', views.ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('contact', views.contact, name='contact'),
]
