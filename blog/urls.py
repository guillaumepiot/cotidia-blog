from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog',

	# Default
	url(r'^$', 'views.latest', name="latest"),
	#url(r'^search/$', 'views.search', name="search"),

	# Categories
	url(r'^categories/$', 'views.categories', name="categories"),
	url(r'^category/(?P<slug>[-\w]+)/$', 'views.category', name="category"),
	
	# Archive
	url(r'^archive/(?P<year>[\d]+)/$', 'views.archive', name="archive_year"),
	url(r'^archive/(?P<year>[\d]+)/(?P<month>[\d]+)/$', 'views.archive', name="archive_month"),

	# Article view
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.article', name="article"),

)