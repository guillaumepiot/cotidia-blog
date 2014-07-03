# Documentation

## Prerequisites

Cotidia blog depends on Cotidia CMS Base and Cotidia Admin Tools. Please those tow modules before installing the blog.

	$ pip install git+https://bitbucket.org/guillaumepiot/cotidia-admin-tools.git
	$ pip install git+https://bitbucket.org/guillaumepiot/cotidia-cms-base.git

##Install

	$ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-blog.git#egg=blog

Migrate

	$ python manage.py migrate blog

In your project settings:

	INSTALLED_APPS = (
		...
		'blog',
		'datetimewidget',
		...
	)

Include the blog url in your url patterns:

	url(r'^blog/', include('blog.urls', namespace='blog')),


## Blog settings

Define the article templates

	BLOG_TEMPLATES = (('blog/article.html', 'Default article'),)

Enable categories

	BLOG_ENABLE_CATEGORIES = getattr(settings, 'BLOG_ENABLE_CATEGORIES', True)

When creating the archive list, decide whether ot not to display years and months with no articles in them
	
	ARCHIVE_SHOW_EMPTY = getattr(settings, 'ARCHIVE_SHOW_EMPTY', False)

When creating the archive list, decide whether ot not to display the articles within each month

	ARCHIVE_SHOW_ARTICLES = getattr(settings, 'ARCHIVE_SHOW_ARTICLES', False)

Show article count next to month

	ARCHIVE_SHOW_COUNT = getattr(settings, 'ARCHIVE_SHOW_COUNT', False)

## Tagging

To enable tagging, you will require the following packages:

django-tagging==0.3.2
django-tagging-autocomplete==0.4

If django-tagging-autocomplete don't install, try from the repo:

	$ pip install git+https://github.com/ludwiktrammer/django-tagging-autocomplete.git


Then enable the tagging setting:

	ENABLE_TAGGING = getattr(settings, 'ENABLE_TAGGING', False)

Add tagging to your INSTALLED_APPS:

	INSTALLED_APPS = (
		...
		'tagging',
		'tagging_autocomplete',
		...
	)

Then sync the database:

	$ python manage.py syncdb

If you are using South for migration, you will need to use this abstraction rule before the Article model:

	# Make this field usable by django south
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])
