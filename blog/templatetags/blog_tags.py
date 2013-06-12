from django import template
register = template.Library()

from blog.models import Article, Category
from blog.utils import Year, Month
from blog import settings as blog_settings

@register.inclusion_tag('blog/includes/_nav.html')
def blog_nav():
    articles = Article.objects.get_published_live().order_by('-publish_date')
    return {'articles': articles}

@register.inclusion_tag('blog/includes/_categories.html')
def blog_categories():
    categories = Category.objects.filter(published=True)
    return {'categories': categories}

@register.inclusion_tag('blog/includes/_archive.html')
def blog_archive():
	archive = {}
	articles = Article.objects.get_published_live().order_by('-publish_date')
	if articles.count() > 0:
		# Get first and last articles
		first = articles[len(articles)-1]
		last = articles[0]
		# Define the earliest and latest years
		earliest_year = first.publish_date.year
		latest_year = last.publish_date.year
		# How many years?
		year_range = latest_year - earliest_year

		# Create year list
		year_list = []
		for i in range(year_range+1):
			year_list.append(Year(latest_year - i))

	return {'archive':year_list, 'show_empty':blog_settings.ARCHIVE_SHOW_EMPTY, 'show_count':blog_settings.ARCHIVE_SHOW_COUNT}


