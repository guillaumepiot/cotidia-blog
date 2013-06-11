from django import template
register = template.Library()

from blog.models import Article, Category

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

		# Create a month list
		month_list = []
		for i in range(12):
			month_list.append(i+1)

		# Create year list
		for i in range(year_range+1):
			#years.append(earliest_year + i)
			archive[earliest_year + i] = month_list

		print archive

	return {'archive':archive}