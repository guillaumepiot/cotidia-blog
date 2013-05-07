from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from cmsbase.views import page_processor

from blog.models import Article, ArticleTranslation

@page_processor(model_class=Article, translation_class=ArticleTranslation)
def article(request, page, slug):
	return render_to_response(page.template, {'page':page,}, context_instance=RequestContext(request))