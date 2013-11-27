Setup
=====

Install
-------

Install from the repository:

 	$ git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-blog.git#egg=blog
 	
Or install in edit mode (best for contributors):

 	$ -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-blog.git#egg=blog

Install the database using the South migrations:

	$ python manage.py migrate blog

URLs
----

urlpatterns = patterns('',
    ...
    url(r'blog/', include('blog.urls', namespace='blog')),
    ...
)

Settings
--------

`BLOG_TEMPLATES`: the list of available blog article templates.

	BLOG_TEMPLATES = (
		('blog/article.html', 'Default article'),
	)