from django import template
register = template.Library()

from blog.models import Article

@register.inclusion_tag('blog/nav.html')
def blog_nav():
    articles = Article.objects.get_published_live().order_by('-publish_date')
    return {'articles': articles}