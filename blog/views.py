from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from localeurl.models import reverse
from django.conf import settings

from cmsbase.views import page_processor

from blog.models import Article, ArticleTranslation, Category, CategoryTranslation, Author
from blog import settings as blog_settings
from blog.utils import MONTH_NAMES

@page_processor(model_class=Article, translation_class=ArticleTranslation)
def article(request, article, slug):

	if not article:
		template = blog_settings.BLOG_TEMPLATES[0][0]
	else:
		template = article.template

	return render_to_response(template, {'article':article,}, context_instance=RequestContext(request))

def latest(request):
	articles = Article.objects.get_published_live().order_by('-publish_date')
	return render_to_response('blog/latest.html', {'articles':articles}, context_instance=RequestContext(request))

def categories(request):
	return render_to_response('blog/categories.html', {}, context_instance=RequestContext(request))

def category(request, slug):
	_category_translation = get_object_or_404(CategoryTranslation, slug=slug, parent__published=True)
	_category = _category_translation.parent
	articles = Article.objects.get_published_live().filter(published_from__categories=_category)
	return render_to_response('blog/category.html', {'category':_category, 'articles':articles}, context_instance=RequestContext(request))

def author(request, slug):

	_author = get_object_or_404(Author, identifier=slug)
	articles = Article.objects.get_published_live().filter(published_from__authors=_author)
	return render_to_response('blog/author.html', {'author':_author, 'articles':articles}, context_instance=RequestContext(request))

def archive(request, year, month=False):
	if month:
		articles = Article.objects.get_published_live().filter(publish_date__year=year, publish_date__month=month).order_by('-publish_date')
		month = MONTH_NAMES[int(month)-1]
	else:
		articles = Article.objects.get_published_live().filter(publish_date__year=year).order_by('-publish_date')

	return render_to_response('blog/archive.html', {'year':year, 'month':month, 'articles':articles}, context_instance=RequestContext(request)) 