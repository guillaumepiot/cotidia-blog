from django.conf.urls import patterns, include, url
from blog.feeds import LatestEntriesFeed

from blog import settings as blog_settings

urlpatterns = patterns('blog',

	# Default
	url(r'^$', 'views.latest', name="latest"),
	#url(r'^search/$', 'views.search', name="search"),

	# Categories
	url(r'^categories/$', 'views.categories', name="categories"),
	url(r'^category/(?P<slug>[-\w]+)/$', 'views.category', name="category"),
	url(r'^tag/$', 'views.tag', name="tag"),

	# Authors
	url(r'^author/(?P<slug>[-\w]+)/$', 'views.author', name="author"),
	
	# Archive
	url(r'^archive/(?P<year>[\d]+)/$', 'views.archive', name="archive_year"),
	url(r'^archive/(?P<year>[\d]+)/(?P<month>[\d]+)/$', 'views.archive', name="archive_month"),

	# RSS feed
	url(r'^feed/$', LatestEntriesFeed(), name="feed"),

	# Article view
	url(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/(?P<day>[\d]+)/(?P<slug>[-\w\/]+)/$', 'views.article', name="article"),
	

)

if blog_settings.ENABLE_TAGGING:
	from tagging_autocomplete.urls import urlpatterns as tagging_patterns
	urlpatterns = urlpatterns + tagging_patterns
	