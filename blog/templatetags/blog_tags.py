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