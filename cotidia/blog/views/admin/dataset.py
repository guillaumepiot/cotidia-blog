import json
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings

from cotidia.account.utils import StaffPermissionRequiredMixin
from cotidia.blog.models import ArticleDataSet
from cotidia.blog.forms.dataset import (
    ArticleDataSetAddForm,
    ArticleDataSetUpdateForm)


###########################
# Article dataset management #
###########################

class ArticleDataSetList(StaffPermissionRequiredMixin, ListView):
    model = ArticleDataSet
    template_name = 'admin/blog/dataset/dataset_list.html'
    permission_required = 'blog.change_articledataset'

    def get_queryset(self):
        return ArticleDataSet.objects.filter()

class ArticleDataSetDetail(StaffPermissionRequiredMixin, DetailView):
    model = ArticleDataSet
    template_name = 'admin/blog/dataset/dataset_detail.html'
    permission_required = 'blog.change_articledataset'

class ArticleDataSetCreate(StaffPermissionRequiredMixin, CreateView):
    model = ArticleDataSet
    form_class = ArticleDataSetAddForm
    template_name = 'admin/blog/dataset/dataset_form.html'
    permission_required = 'blog.add_articledataset'

    def get_success_url(self):
        messages.success(self.request, _('ArticleDataSet has been created.'))
        return reverse('blog-admin:articledataset-detail', kwargs={'pk':self.object.id})

class ArticleDataSetUpdate(StaffPermissionRequiredMixin, UpdateView):
    model = ArticleDataSet
    form_class = ArticleDataSetUpdateForm
    template_name = 'admin/blog/dataset/dataset_form.html'
    permission_required = 'blog.change_articledataset'

    def get_success_url(self):
        messages.success(self.request, _('ArticleDataSet details have been updated.'))
        return reverse('blog-admin:articledataset-detail', kwargs={'pk':self.object.id})

class ArticleDataSetDelete(StaffPermissionRequiredMixin, DeleteView):
    model = ArticleDataSet
    permission_required = 'blog.delete_articledataset'
    template_name = 'admin/blog/dataset/dataset_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _('ArticleDataSet has been deleted.'))
        return reverse('blog-admin:articledataset-list')
