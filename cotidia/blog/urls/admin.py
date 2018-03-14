from django.conf.urls import url

from cotidia.blog.views.admin.article import *
from cotidia.blog.views.admin.dataset import *
from cotidia.blog.views.admin.article_title import (
    ArticleTitleCreate,
    ArticleTitleUpdate
)
from cotidia.blog.views.admin.article_url import (
    ArticleURLUpdate
)

app_name = 'blog'

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='article-list'),
    url(r'^article/add/$', ArticleCreate.as_view(), name='article-add'),
    url(r'^article/(?P<pk>[\d]+)/$', ArticleDetail.as_view(), name='article-detail'),
    url(r'^article/(?P<pk>[\d]+)/update/$', ArticleUpdate.as_view(), name='article-update'),
    url(r'^article/(?P<pk>[\d]+)/delete/$', ArticleDelete.as_view(), name='article-delete'),

    url(r'^article/(?P<article_id>[\d]+)/meta-data/(?P<language_code>[-\w]+)/', add_edit_translation, name='article-metadata-update'),

    url(r'^article/(?P<parent_id>[\d]+)/(?P<lang>[-\w]+)/url/(?P<pk>[\d]+)/update/$',
        ArticleURLUpdate.as_view(), name='article-url-update'),

    url(r'^article/(?P<parent_id>[\d]+)/(?P<lang>[-\w]+)/title/add/$',
        ArticleTitleCreate.as_view(), name='article-title-add'),
    url(r'^article/(?P<parent_id>[\d]+)/(?P<lang>[-\w]+)/title/(?P<pk>[\d]+)/update/$',
        ArticleTitleUpdate.as_view(), name='article-title-update'),

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
