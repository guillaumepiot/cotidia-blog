from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from cmsbase.views import page_processor

from blog.models import Article, ArticleTranslation, Category, CategoryTranslation
from blog import settings as blog_settings

@page_processor(model_class=Article, translation_class=ArticleTranslation)
def article(request, page, slug):

	# Raise a 404 if the page can't be found
	if not page:
		template = blog_settings.BLOG_TEMPLATES[0][0]
	else:
		template = page.template

	return render_to_response(template, {'page':page,}, context_instance=RequestContext(request))

def categories(request):
	return render_to_response('blog/categories.html', {}, context_instance=RequestContext(request))

def category(request, slug):
	_category_translation = get_object_or_404(CategoryTranslation, slug=slug, parent__published=True)
	_category = _category_translation.parent
	articles = Article.objects.get_published_live().filter(categories=_category)
	return render_to_response('blog/category.html', {'category':_category, 'articles':articles}, context_instance=RequestContext(request))