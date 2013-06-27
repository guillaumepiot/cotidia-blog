Templates
=========

Template tags
-------------

### Inclusion tags

`blog_nav` renders a navigation list of all the published articles

	{% blog_nav %}

`blog_categories` renders a list of all published categories

	{% blog_categories %}
	
`blog_archive` renders a chronological archive. 

	{% blog_archive %}
	
Options:

A few options are available to dictate the content of the archive:
	
	# When creating the archive list, decide whether ot not to display years and months with no articles in them
	ARCHIVE_SHOW_EMPTY = getattr(settings, 'ARCHIVE_SHOW_EMPTY', False)
	# When creating the archive list, decide whether ot not to display the articles within each month
	ARCHIVE_SHOW_ARTICLES = getattr(settings, 'ARCHIVE_SHOW_ARTICLES', False)
	# Show article count next to month
	ARCHIVE_SHOW_COUNT = getattr(settings, 'ARCHIVE_SHOW_COUNT', False)

You can also pass those options on a tag basis by passing extra arguments to the template tag:

	{% blog_archive 'show_empty' 'show_articles' 'show_count' %}
	
For example, an archive that shows the articles and the article count per year & month will be:
	
	{% blog_archive 0 1 1 %}
	
	
`get_latest_articles` populate the template context with a list of latest articles.

	{% get_latest_articles 'limit' as latest_articles %}
	
Eg:
	
	{% get_latest_articles '1' as latest_articles %}
	{% for article in latest_articles %}
		{{article}}
	{% endfor %}
