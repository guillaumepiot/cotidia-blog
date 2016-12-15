Setup
=====

Install
-------

Install from the repository:

 	$ git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-blog.git#egg=blog
 	
Or install in edit mode (best for contributors):

 	$ -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-blog.git#egg=blog

Install the database using the migrations:

	$ python manage.py migrate blog

URLs
----

urlpatterns = patterns('',
    ...
    url(r'^admin/blog/', include('blog.urls.admin', namespace='blog-admin')),
    url(r'^blog/', include('blog.urls.public', namespace='blog-public')),
    ...
)

Settings
--------

`BLOG_TEMPLATES`: the list of available blog article templates.

	BLOG_TEMPLATES = (
		('blog/article.html', 'Default article'),
	)