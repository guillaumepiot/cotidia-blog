from django.conf import settings

# The default page templates
BLOG_TEMPLATES = getattr(settings, 'BLOG_TEMPLATES', (('blog/article.html', 'Default article'),))