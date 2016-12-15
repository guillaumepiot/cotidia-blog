from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.db import transaction
from django.conf import settings

from cotidia.account.utils import StaffPermissionRequiredMixin

from cotidia.cms.settings import CMS_LANGUAGES

from cotidia.blog.models import Article, ArticleTranslation
from cotidia.blog.forms.article import (
    ArticleAddForm,
    ArticleUpdateForm,
    ArticleURLForm,
    ArticleTitleForm
    )
from cotidia.blog.forms.custom_form import TranslationForm


class ArticleList(StaffPermissionRequiredMixin, ListView):
    model = Article
    template_name = 'admin/blog/article_list.html'
    permission_required = 'blog.change_article'

    def get_queryset(self):
        return Article.objects.get_originals()


class ArticleDetail(StaffPermissionRequiredMixin, DetailView):
    model = Article
    template_name = 'admin/blog/article_detail.html'
    permission_required = 'blog.change_article'


class ArticleCreate(StaffPermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleAddForm
    template_name = 'admin/blog/article_form.html'
    permission_required = 'blog.add_article'

    def get_success_url(self):
        messages.success(self.request, _('The page has been created.'))
        return reverse('blog-admin:article-list')


class ArticleUpdate(StaffPermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleUpdateForm
    template_name = 'admin/blog/article_form.html'
    permission_required = 'blog.change_article'

    def get_success_url(self):
        messages.success(self.request, _('The page details have been updated.'))
        return reverse('blog-admin:article-detail', kwargs={'pk':self.object.id})

    def post(self, request, *args, **kwargs):
        response = super(ArticleUpdate, self).post(request, *args, **kwargs)
        if self.object.get_translations:
            self.object.approval_needed = True
            self.object.save()
        return response

class ArticleDelete(StaffPermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = 'blog.delete_article'
    template_name = 'admin/blog/article_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _('The page has been deleted.'))
        return reverse('blog-admin:article-list')



@login_required
@transaction.atomic()
def add_edit_translation(
    request,
    article_id,
    language_code,
    model_class=Article,
    translation_class=ArticleTranslation,
    translation_form_class=TranslationForm):

    if not language_code in [lang[0] for lang in CMS_LANGUAGES]:
        raise ImproperlyConfigured('The language code "%s" is not included in the project settings.' % language_code)
    if not request.user.has_perm('blog.add_articletranslation'):
        raise PermissionDenied
    page = get_object_or_404(model_class, id=article_id)

    translation = translation_class.objects.filter(parent=page, language_code=language_code).first()

    initial = {
        'parent':page,
        'language_code':language_code
    }

    # Check is we are in revision mode
    # if recover_id:
    #     recover = True
    #     for version in reversion.get_unique_for_object(translation):
    #         if version.id == int(recover_id):
    #             # Set values from revision
    #             translation.title = version.field_dict['title']
    #             translation.slug = version.field_dict['slug']
    #             translation.content = version.field_dict['content']
    # else:
    #     recover = False

    if not translation:
        title = _('Add translation')
        form = translation_form_class(page=page, initial=initial)
    else:
        title = _('Edit translation')
        if not request.user.has_perm('cmsbase.change_articletranslation'):
            raise PermissionDenied

        form = translation_form_class(instance=translation, page=page, initial=initial)

    if request.method == 'POST':
        if not translation:
            form = translation_form_class(data=request.POST, files=request.FILES, page=page)
        else:
            form = translation_form_class(data=request.POST, files=request.FILES, instance=translation, page=page)
        if form.is_valid():
            translation = form.save()
            # reversion.set_user(request.user)

            # Notify the parent page that new content needs to be approved
            translation.parent.approval_needed = 1
            translation.parent.save()

            # if recover:
            #     messages.add_message(request, messages.SUCCESS, _('The content for "%s" has been recovered' % translation.title))
            # else:
            #     messages.add_message(request, messages.SUCCESS, _('The content for "%s" has been saved' % translation.title))
            messages.add_message(request, messages.SUCCESS, _('The meta data for "%s" has been saved' % translation.title))
            return HttpResponseRedirect(reverse('blog-admin:article-detail', kwargs={'pk':page.id}))




    template = 'admin/blog/article_metadata_form.html'
    context={
        'form':form,
        #'title':title,
        'page':page,
        'translation':translation,
        #'recover':recover,
        #'app_label':page._meta.app_label,
        #'model_name':page._meta.model_name,
        #'verbose_name_plural':page._meta.verbose_name_plural
    }
    return render_to_response(template, context, context_instance=RequestContext(request))

##############
# Publishing #
##############

@permission_required('blog.publish_article', settings.ADMIN_LOGIN_URL)
def ArticlePublish(request, article_id):

    page = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        if page.get_translations():

            page.approval_needed = False
            page.published = True
            page.save()
            page.publish_version()
            page.publish_translations()

            messages.success(request, _('The page has been published.'))

        return HttpResponseRedirect(
            reverse('blog-admin:article-detail', kwargs={'pk': page.id}))

    template = 'admin/blog/article_publish_form.html'

    return render_to_response(template, {'page':page},
        context_instance=RequestContext(request))

@permission_required('blog.publish_article', settings.ADMIN_LOGIN_URL)
def ArticleUnpublish(request, article_id):

    page = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        if page.get_translations():

            page.approval_needed = False
            page.published = False
            page.save()
            page.unpublish_version()

            messages.success(request, _('The page has been unpublished.'))

        return HttpResponseRedirect(
            reverse('blog-admin:article-detail', kwargs={'pk': page.id}))

    template = 'admin/blog/article_unpublish_form.html'

    return render_to_response(template, {'page':page},
        context_instance=RequestContext(request))

###########
# Content #
###########

@permission_required('blog.add_articletranslation', settings.ADMIN_LOGIN_URL)
def ArticleURLCreate(request, article_id, lang):

    page = get_object_or_404(Article, id=article_id)

    form = ArticleURLForm()

    if request.method == 'POST':
        form = ArticleURLForm(request.POST)

        if form.is_valid():
            translation = form.save(commit=False)
            translation.parent = page
            translation.language_code = lang
            translation.save()

            page.approval_needed = True
            page.save()

            messages.success(request, _('The page URL has been saved.'))

            return HttpResponseRedirect(
                reverse('blog-admin:article-detail', kwargs={'pk': page.id}))

    template = 'admin/blog/article_url_form.html'

    return render_to_response(template, {'form':form, 'page':page},
        context_instance=RequestContext(request))

@permission_required('blog.change_articletranslation', settings.ADMIN_LOGIN_URL)
def ArticleURLUpdate(request, article_id, lang, trans_id):

    page = get_object_or_404(Article, id=article_id)
    translation = get_object_or_404(ArticleTranslation, id=trans_id)

    form = ArticleURLForm(instance=translation)

    if request.method == 'POST':
        form = ArticleURLForm(request.POST, instance=translation)

        if form.is_valid():
            translation = form.save(commit=False)
            translation.parent = page
            translation.language_code = lang
            translation.save()

            page.approval_needed = True
            page.save()

            messages.success(request, _('The page URL has been saved.'))

            return HttpResponseRedirect(
                reverse('blog-admin:article-detail', kwargs={'pk': page.id}))

    template = 'admin/blog/article_url_form.html'

    return render_to_response(template, {
        'form':form, 'page':page, 'translation':translation},
        context_instance=RequestContext(request))

#
# Manage the page title for a language
#
@permission_required('blog.change_article', settings.ADMIN_LOGIN_URL)
def ArticleTitleUpdate(request, article_id, lang, trans_id=None):

    page = get_object_or_404(Article, id=article_id)
    if trans_id:
        translation = get_object_or_404(ArticleTranslation, id=trans_id)
        form = ArticleTitleForm(instance=translation)
    else:
        translation = None
        form = ArticleTitleForm()

    if request.method == 'POST':

        if translation:
            form = ArticleTitleForm(instance=translation, data=request.POST)
        else:
            form = ArticleTitleForm(data=request.POST)

        if form.is_valid():

            translation = form.save(commit=False)
            translation.parent = page
            translation.language_code = lang
            if not translation.slug:
                translation.slug = slugify(translation.title.lower())
            translation.save()


            page.approval_needed = True
            page.save()

            messages.success(request, _('The page title has been saved.'))

            return HttpResponseRedirect(
                reverse('blog-admin:article-detail', kwargs={'pk': page.id}))

    template = 'admin/blog/article_title_form.html'

    return render_to_response(template, {'form':form, 'page':page},
        context_instance=RequestContext(request))
