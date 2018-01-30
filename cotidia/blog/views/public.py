import datetime

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from cotidia.cms.views.public import get_page
from cotidia.cms.conf import settings

from cotidia.blog.models import Article, ArticleTranslation
from cotidia.blog import settings as blog_settings
from cotidia.blog.utils import MONTH_NAMES


# Page decorator
# Cover the basic handling such as page object lookup, redirect, 404,
# preview mode, language switching url switching
def blog_processor(model_class=Article, translation_class=ArticleTranslation):
    def wrap(f):
        def wrapper(request, year, month, day, slug, *args, **kwargs):

            # Check if the preview variable is in the path
            preview = request.GET.get('preview', False)

            # Set preview to False by default
            is_preview = False

            # Make sure the user has the right to see the preview
            if request.user.is_authenticated and preview is not False:
                is_preview = True

            date = datetime.datetime(
                year=int(year),
                month=int(month),
                day=int(day))

            filter_args = {
                'parent__publish_date__range':
                    (
                        datetime.datetime.combine(date, datetime.time.min),
                        datetime.datetime.combine(date, datetime.time.max)
                    )
            }

            # Is it home page or not?
            page = get_page(
                request=request,
                model_class=model_class,
                translation_class=translation_class,
                slug=slug,
                preview=is_preview,
                filter_args=filter_args)

            # Check if any page exists at all
            # Then Raise a 404 if no page can be found
            if not page:
                raise Http404('This article does not exists')

            else:
                # The publish date must be in the past to be available
                if not page.is_published() and is_preview is False:
                    raise Http404('This article is not published yet')
                # Hard redirect if specified in page attributes
                if page.redirect_to:
                    return HttpResponseRedirect(
                        page.redirect_to.get_absolute_url())
                if page.redirect_to_url:
                    return HttpResponseRedirect(
                        page.redirect_to_url)

                # When you switch language it will load the right translation
                # but stay on the same slug.  So we need to redirect to the
                # right translated slug if not on it already
                page_url = page.get_absolute_url()

                if not page_url == request.path and slug \
                        and not settings.CMS_PREFIX:
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

    return render(request, template, {'page': article})


def latest(request):
    articles = Article.objects.get_published_live().order_by('-publish_date')
    return render(request, 'blog/latest.html', {'articles': articles})


def archive(request, year, month=False):
    if month:
        articles = Article.objects.get_published_live().filter(
            publish_date__year=year,
            publish_date__month=month).order_by('-publish_date')
        month = MONTH_NAMES[int(month) - 1]
    else:
        articles = Article.objects.get_published_live().filter(
            publish_date__year=year).order_by('-publish_date')

    return render(
        request,
        'blog/archive.html',
        {'year': year, 'month': month, 'articles': articles}
    )
