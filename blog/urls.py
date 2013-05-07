from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog',

	url(r'^$', 'views.article', name="latest"),
	#url(r'^search/$', 'views.search', name="search"),
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.article', name="article"),

)