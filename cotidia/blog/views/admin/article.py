import django_filters

from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from cotidia.account.conf import settings
from cotidia.admin.views import (
    AdminListView,
    AdminDetailView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)
from cotidia.blog.models import Article
from cotidia.blog.forms.admin.article import (
    ArticleAddForm,
    ArticleUpdateForm
)


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

    def get_fieldsets(self):
        fieldsets = self.fieldsets.copy()

        if settings.CMS_ENABLE_META_DATA:
            fieldsets.insert(1, {
                "legend": "Meta data",
                "template_name": "admin/blog/article/metadata.html"
            })

        return fieldsets


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


class ArticleDelete(AdminDeleteView):
    model = Article


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
