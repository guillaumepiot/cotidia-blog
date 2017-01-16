from django import template

from cotidia.blog.models import Article
from cotidia.blog.utils import Year
from cotidia.blog import settings as blog_settings

register = template.Library()


@register.inclusion_tag('blog/includes/_nav.html')
def blog_nav():
    articles = Article.objects.get_published_live().order_by('-publish_date')
    return {'articles': articles}


@register.inclusion_tag('blog/includes/_archive.html', takes_context=True)
def blog_archive(
        context,
        show_empty=blog_settings.ARCHIVE_SHOW_EMPTY,
        show_articles=blog_settings.ARCHIVE_SHOW_ARTICLES,
        show_count=blog_settings.ARCHIVE_SHOW_COUNT
        ):
    year_list = []
    articles = Article.objects.get_published_live().order_by('-publish_date')
    request = context['request']
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
        for i in range(year_range+1):
            year_list.append(Year(latest_year - i))

    return {
        'archive': year_list,
        'request': request,
        'show_empty': show_empty,
        'show_articles': show_articles,
        'show_count': show_count
        }


@register.assignment_tag
def get_latest_article():
    return Article.objects.get_published_live().latest('publish_date')


@register.assignment_tag
def get_next_article(current_article):

    if current_article.published_from is None:
        current_article = Article.objects.filter(
            published_from=current_article).first()

    if current_article:
        queryset = Article.objects.get_published_live().filter(
            publish_date__gte=current_article.publish_date).exclude(
            id=current_article.id).order_by('publish_date')
        if queryset.count():
            return queryset.first()

    return None


@register.assignment_tag
def get_previous_article(current_article):

    if current_article.published_from is None:
        current_article = Article.objects.filter(
            published_from=current_article).first()

    if current_article:
        queryset = Article.objects.get_published_live().filter(
            publish_date__lte=current_article.publish_date).exclude(
            id=current_article.id)

        if queryset.count():
            return queryset.latest('publish_date')

    return None


@register.assignment_tag
def get_latest_articles(limit=3):
    return Article.objects.get_published_live().order_by(
        '-publish_date')[:int(limit)]


@register.assignment_tag
def get_latest_articles_per_language(language, limit=False):
    from django.utils.translation import get_language
    articles = Article.objects.get_published_translation_live(
        language_code=get_language()).order_by('-parent__publish_date')
    if limit:
        articles = articles[:int(limit)]
    return articles


@register.assignment_tag
def get_latest_by_author(author, limit=3, exclude=False):

    queryset = Article.objects.get_published_live().filter(
        published_from__authors=author)

    if exclude:
        return queryset.exclude(
            id=exclude.id).order_by('-publish_date')[:int(limit)]
    else:
        return queryset.order_by(
            '-publish_date')[:int(limit)]
