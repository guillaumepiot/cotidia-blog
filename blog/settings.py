from django.conf import settings

# The default page templates
BLOG_TEMPLATES = getattr(settings, 'BLOG_TEMPLATES', (('blog/article.html', 'Default article'),))

# When creating the archive list, decide whether ot not to display years and months with no articles in them
ARCHIVE_SHOW_EMPTY = getattr(settings, 'ARCHIVE_SHOW_EMPTY', False)
# When creating the archive list, decide whether ot not to display the articles within each month
ARCHIVE_SHOW_ARTICLES = getattr(settings, 'ARCHIVE_SHOW_ARTICLES', False)
# Show article count next to month
ARCHIVE_SHOW_COUNT = getattr(settings, 'ARCHIVE_SHOW_COUNT', False)