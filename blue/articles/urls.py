from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='homepage'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article'),
    path('redaction', views.redaction, name='redaction'),
    path('redaction_article', views.RedactionArticleListView.as_view(), name='redaction_article'),
    path('article_create', views.ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('redaction_short', views.RedactionShortListView.as_view(), name='redaction_short'),
    path('short_create', views.ShortCreateView.as_view(), name='short_create'),
    path('short_update/<int:pk>', views.ShortUpdateView.as_view(), name='short_update'),
    path('short_delete/<int:pk>', views.ShortDeleteView.as_view(), name='short_delete'),
    path('redaction_useful_link', views.RedactionUsefulLinkListView.as_view(), name='redaction_useful_link'),
    path('useful_link_create', views.UsefulLinkCreateView.as_view(), name='useful_link_create'),
    path('useful_link_update/<int:pk>', views.UsefulLinkUpdateView.as_view(), name='useful_link_update'),
    path('useful_link_delete/<int:pk>', views.UsefulLinkDeleteView.as_view(), name='useful_link_delete'),
    path('redaction_asset', views.RedactionAssetListView.as_view(), name='redaction_asset'),
    path('asset_create', views.AssetCreateView.as_view(), name='asset_create'),
    path('asset_update/<int:pk>', views.AssetUpdateView.as_view(), name='asset_update'),
    path('asset_delete/<int:pk>', views.AssetDeleteView.as_view(), name='asset_delete'),
    path('contact', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
