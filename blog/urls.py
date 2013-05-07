from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog',

	url(r'^$', 'views.article', name="latest"),
	#url(r'^search/$', 'views.search', name="search"),
	url(r'^categories/$', 'views.categories', name="categories"),
	url(r'^category/(?P<slug>[-\w]+)/$', 'views.category', name="category"),
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.article', name="article"),

)