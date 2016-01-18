import datetime

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from cms.views.public import page_processor, get_page
from cms import settings as cms_settings

from blog.models import Article, ArticleTranslation
from blog import settings as blog_settings
from blog.utils import MONTH_NAMES


# Page decorator
# Cover the basic handling such as page object lookup, redirect, 404, preview mode, language switching url switching
def blog_processor(model_class=Article, translation_class=ArticleTranslation):
	def wrap(f):
		def wrapper(request, year, month, day, slug, *args, **kwargs):

			# Check if the preview variable is in the path
			preview = request.GET.get('preview', False)

			# Set preview to False by default
			is_preview = False

			# Make sure the user has the right to see the preview
			if request.user.is_authenticated() and not preview == False:
				is_preview = True

			date = datetime.datetime(year=int(year), month=int(month), day=int(day))
			filter_args = {'parent__publish_date__range': (datetime.datetime.combine(date, datetime.time.min),
                            datetime.datetime.combine(date, datetime.time.max))} 

			# Is it home page or not?
			page = get_page(request=request, model_class=model_class, translation_class=translation_class, slug=slug, preview=is_preview, filter_args=filter_args)

			# Check if any page exists at all
			# Then Raise a 404 if no page can be found
			if not page:
				raise Http404('This article does not exists')

			else:
				# The publish date must be in the past to be available
				if not page.is_published() and is_preview == False:
					raise Http404('This article is not published yet')
				# Hard redirect if specified in page attributes
				if page.redirect_to:
					return HttpResponseRedirect(page.redirect_to.get_absolute_url())
				if page.redirect_to_url:
					return HttpResponseRedirect(page.redirect_to_url)

				# When you switch language it will load the right translation but stay on the same slug
				# So we need to redirect to the right translated slug if not on it already
				page_url = page.get_absolute_url()

				if not page_url == request.path and slug and not cms_settings.CMS_PREFIX:
					return HttpResponseRedirect(page_url)

			# Assign is_preview to the request object for cleanliness
			request.is_preview = is_preview

			return f(request, page, year, month, day, slug, *args, **kwargs)
		return wrapper
	return wrap


@blog_processor(model_class=Article, translation_class=ArticleTranslation)
def article(request, article, year, month, day, slug):

	if not article:
		template = blog_settings.BLOG_TEMPLATES[0][0]
	else:
		template = article.template

	return render_to_response(template, {'page':article,}, context_instance=RequestContext(request))

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

def tag(request):
	if not request.GET.get('tag'):
		return HttpResponseRedirect(reverse('blog:latest'))
	else:
		slug = request.GET.get('tag')
		from django.utils.translation import get_language
		tag = get_object_or_404(Tag, name=slug)
		queryset = ArticleTranslation.objects.filter(language_code=get_language()).exclude(parent__published_from=None)
		queryset = TaggedItem.objects.get_by_model(queryset, tag)

	return render_to_response('blog/tag.html', {'tag':tag, 'articles':queryset}, context_instance=RequestContext(request))


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