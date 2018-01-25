from django.conf.urls import url

from cotidia.blog.views.admin import *
from cotidia.blog.views.dataset import *

app_name = 'blog'

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='article-list'),
    url(r'^article/add/$', ArticleCreate.as_view(), name='article-add'),
    url(r'^article/(?P<pk>[\d]+)/$', ArticleDetail.as_view(), name='article-detail'),
    url(r'^article/(?P<pk>[\d]+)/update/$', ArticleUpdate.as_view(), name='article-update'),
    url(r'^article/(?P<pk>[\d]+)/delete/$', ArticleDelete.as_view(), name='article-delete'),

    url(r'^article/(?P<article_id>[\d]+)/meta-data/(?P<language_code>[-\w]+)/', add_edit_translation, name='article-metadata-update'),

    url(r'^article/(?P<article_id>[\d]+)/(?P<lang>[-\w]+)/url/add/$',
        ArticleURLCreate, name='article-url-add'),
    url(r'^article/(?P<article_id>[\d]+)/(?P<lang>[-\w]+)/url/(?P<trans_id>[\d]+)/update/$',
        ArticleURLUpdate, name='article-url-update'),

    url(r'^article/(?P<article_id>[\d]+)/(?P<lang>[-\w]+)/title/add/$',
        ArticleTitleUpdate, name='article-title-add'),
    url(r'^article/(?P<article_id>[\d]+)/(?P<lang>[-\w]+)/title/(?P<trans_id>[\d]+)/update/$',
        ArticleTitleUpdate, name='article-title-update'),

    url(r'^article/(?P<article_id>[\d]+)/publish/$',
        ArticlePublish, name='article-publish'),

    url(r'^article/(?P<article_id>[\d]+)/unpublish/$',
        ArticleUnpublish, name='article-unpublish'),

    url(r'^dataset/$', ArticleDataSetList.as_view(), name='articledataset-list'),
    url(r'^dataset/add/$', ArticleDataSetCreate.as_view(), name='articledataset-add'),
    url(r'^dataset/(?P<pk>[\d]+)/$', ArticleDataSetDetail.as_view(), name='articledataset-detail'),
    url(r'^dataset/(?P<pk>[\d]+)/update/$', ArticleDataSetUpdate.as_view(), name='articledataset-update'),
    url(r'^dataset/(?P<pk>[\d]+)/delete/$', ArticleDataSetDelete.as_view(), name='articledataset-delete'),
]
