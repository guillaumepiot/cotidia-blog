import django_filters

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.db import transaction

from cotidia.account.utils import StaffPermissionRequiredMixin
from cotidia.account.conf import settings
from cotidia.admin.views import AdminListView
from cotidia.admin.mixins import StaffPermissionRequiredMixin
from cotidia.admin.views import (
    AdminListView,
    AdminDetailView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)
from cotidia.blog.models import Article, ArticleTranslation
from cotidia.blog.forms.admin.article import (
    ArticleAddForm,
    ArticleUpdateForm,
    ArticleURLForm,
    ArticleTitleForm
)
from cotidia.blog.forms.custom_form import TranslationForm


class ArticleFilter(django_filters.FilterSet):
    display_title = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Search"
    )

    class Meta:
        model = Article
        fields = ['display_title']


class ArticleList(AdminListView):
    model = Article
    columns = (
        ('Title', 'display_title'),
        ('URL', 'get_absolute_url'),
        ('Status', 'status'),
        ('Publish date', 'publish_date'),
    )
    template_type = "fluid"
    filterset = ArticleFilter
    actions = ["approve"]
    row_click_action = "detail"
    row_actions = ["view"]

    def get_queryset(self):
        queryset = Article.objects.get_originals()

        if self.filterset:
            self.filter = self.filterset(
                self.request.GET,
                queryset=queryset
            )
            queryset = self.filter.qs

        return queryset.order_by('-publish_date')

    def approve(self, object):
        if object.get_translations():
            object.approval_needed = False
            object.published = True
            object.save()
            object.publish_version()
            object.publish_translations()

    approve.action_name = "Approve & Publish"


class ArticleDetail(AdminDetailView):
    model = Article
    fieldsets = [
        {
            "legend": "Content",
            "template_name": "admin/blog/article/content.html"
        },
        {
            "legend": "Meta data",
            "template_name": "admin/cms/page/metadata.html"
        },
        {
            "legend": "Dataset",
            "template_name": "admin/blog/article/dataset.html"
        },
        {
            "legend": "Settings",
            "fields": [
                [
                    {
                        "label": "Display title",
                        "field": "display_title",
                    },
                    {
                        "label": "Template",
                        "field": "template",
                    }
                ],
                [
                    {
                        "label": "Publish date",
                        "field": "publish_date",
                    },
                    {
                        "label": "Author",
                        "field": "author",
                    }
                ],
                {
                    "label": "Unique page identifier",
                    "field": "slug",
                },
            ]
        }
    ]


class ArticleCreate(AdminCreateView):
    model = Article
    form_class = ArticleAddForm


class ArticleUpdate(AdminUpdateView):
    model = Article
    form_class = ArticleUpdateForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.get_translations:
            self.object.approval_needed = True
            self.object.save()
        return response

    def get_success_url(self):
        messages.success(self.request, _('The page has been deleted.'))
        return reverse('blog-admin:article-detail', kwargs={'pk': self.object.id})


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

    if language_code not in [lang[0] for lang in settings.CMS_LANGUAGES]:
        raise ImproperlyConfigured('The language code "%s" is not included in the project settings.' % language_code)
    if not request.user.has_perm('blog.add_articletranslation'):
        raise PermissionDenied
    page = get_object_or_404(model_class, id=article_id)

    translation = translation_class.objects.filter(parent=page, language_code=language_code).first()

    initial = {
        'parent': page,
        'language_code': language_code
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

    context = {
        'form': form,
        'page': page,
        'translation': translation,
    }
    return render(request, template, context)


@permission_required('blog.publish_article', settings.ACCOUNT_ADMIN_LOGIN_URL)
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

    template = 'admin/blog/article/form_publish.html'

    return render(request, template, {'page': page})


@permission_required('blog.publish_article', settings.ACCOUNT_ADMIN_LOGIN_URL)
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

    template = 'admin/blog/article/form_unpublish.html'

    return render(request, template, {'page': page})
