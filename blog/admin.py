import reversion

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.admin.views.main import ChangeList

from mptt.admin import MPTTModelAdmin
from multilingual_model.admin import TranslationInline

from redactor.widgets import RedactorEditor
from datetimewidget.widgets import DateTimeWidget

from cmsbase.admin import PageAdmin, PageFormAdmin, PublishingWorkflowAdmin, PageDataSetAdminForm
from cmsbase.admin_forms import TranslationForm 
from cmsbase.widgets import AdminImageWidget, AdminCustomFileWidget

from blog.models import *
from blog import settings as blog_settings

from filemanager.widgets import MultipleFileWidget

if blog_settings.ENABLE_TAGGING:
    from tagging.forms import TagField
    from blog.widgets import TagAutocomplete

class ArticleTranslationForm(TranslationForm):
    class Meta:
        model = ArticleTranslation
        exclude = ['content']

    def __init__(self, *args, **kwargs):
        super(ArticleTranslationForm, self).__init__(*args, **kwargs)
        if blog_settings.ENABLE_TAGGING:
            self.fields['tags'] = TagField(widget=TagAutocomplete(), required=False, help_text=_('Please enter a list of comma separated keywords.'))
            # Add tags to the fieldsets
            self._fieldsets[0][1]['fields'].append('tags')

class ArticleAdminForm(PageFormAdmin):
    publish_date = forms.DateTimeField(widget=DateTimeWidget(attrs={'id':"datetime-picker"}, usel10n = True))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(), widget=forms.CheckboxSelectMultiple, required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.filter(), widget=forms.CheckboxSelectMultiple, required=False)
    images = forms.CharField(widget=MultipleFileWidget, required=False)
    class Meta:
        model = Article

    def __init__(self, *args, **kwargs):
        from django.contrib.contenttypes.models import ContentType
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        if not blog_settings.BLOG_ENABLE_CATEGORIES:
            del self.fields['categories']

        if self.instance:
            content_type = ContentType.objects.get_for_model(self.instance)
            object_pk = self.instance.id
            self.fields['images'].widget.attrs.update({'content_type':content_type.id, 'object_pk':object_pk})
        else:
            self.fields['images'].widget.attrs.update({'content_type':False, 'object_pk':False})


        
class ArticleAdmin(reversion.VersionAdmin, PublishingWorkflowAdmin):
    form = ArticleAdminForm
    translation_form_class = ArticleTranslationForm
    
    ordering = ['-publish_date'] 

    # Override the list display from PublishingWorkflowAdmin
    def get_list_display(self, request, obj=None):
        if not settings.PREFIX_DEFAULT_LOCALE:
            return ['title', 'is_published', 'approval', 'publish_date', 'template']
        else:
            return ['title', 'is_published', 'approval', 'publish_date', 'template', 'languages']

    fieldsets = (
        
        ('Settings', {
            'classes': ('default',),
            'fields': ('display_title', 'template', 'dataset',  'parent', 'publish_date' )
        }),
        ('Authors', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('authors',)
        }),
        ('Images', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('images',)
        }),

    )

    if blog_settings.BLOG_ENABLE_CATEGORIES:
        fieldsets = fieldsets + (
            ('Categories', {
                #'description':_('The page template'),
                'classes': ('default',),
                'fields': ('categories',)
            }),
        )
    # if blog_settings.ENABLE_TAGGING:
    #     fieldsets = fieldsets + (
    #         ('', {
    #             'classes': ('default',),
    #             'fields': ('tags',)
    #         }),
    #     )

    class Media:
        css = {
            "all": ("admin/css/page.css",)
        }
        js = ("admin/js/page.js",)

    # def get_urls(self):
    #     from django.conf.urls import patterns, url
    #     urls = super(ArticleAdmin, self).get_urls()
    #     my_urls = patterns('',
    #         url(r'translation/(?P<page_id>[-\w]+)/(?P<language_code>[-\w]+)/', self.admin_site.admin_view(add_edit_translation), {'translation_class':self.model.CMSMeta.translation_class}, name='add_edit_translation' ),
    #     )
    #     return my_urls + urls

admin.site.register(Article, ArticleAdmin)



class ArticleDataSetAdmin(reversion.VersionAdmin):
    form = PageDataSetAdminForm


admin.site.register(ArticleDataSet, ArticleDataSetAdmin)



# Category translation

class CategoryTranslationInline(TranslationInline):
    model = CategoryTranslation
    prepopulated_fields = {'slug': ('title',)}



# Category

class CategoryForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'errorfield'
    class Meta:
        model = Category

class CategoryAdmin(MPTTModelAdmin):
    form = CategoryForm
    list_display = ["title", "identifier", "published", 'order_id', 'languages']
    inlines = (CategoryTranslationInline, )
    mptt_indent_field = 'title'
    mptt_level_indent = 20

    def title(self, obj):
        translation = obj.translated() #PageTranslation.objects.filter(parent=obj, language_code=settings.DEFAULT_LANGUAGE)
        if translation:
            return translation.title
        else:
            return _('No translation available for default language')

    def languages(self, obj):
        ts=[]
        for t in obj.get_translations():
            ts.append(u'<img src="/static/admin/img/flags/%s.png" alt="" rel="tooltip" data-title="%s">' % (t.language_code, t.__unicode__()))
        return ' '.join(ts)

    languages.allow_tags = True
    languages.short_description = 'Translations'

    # Override the list display from PublishingWorkflowAdmin
    def get_list_display(self, request, obj=None):
        if not settings.PREFIX_DEFAULT_LOCALE:
            return ["title", "identifier", "published", 'order_id']
        else:
            return ["title", "identifier", "published", 'order_id', 'languages']

    fieldsets = (

        
        ('Settings', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('published', 'parent', 'order_id', 'identifier', )
        }),

    )

    class Media:
        css = {
            "all": ("admin/css/page.css",)
        }
        js = ("admin/js/page.js",)

if blog_settings.BLOG_ENABLE_CATEGORIES:
    admin.site.register(Category, CategoryAdmin)


# Author translation

class AuthorTranslationInline(TranslationInline):
    model = AuthorTranslation

class AuthorForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'errorfield'
    photo = forms.ImageField(label=_('Photo'), widget=AdminImageWidget, required=False)
    class Meta:
        model = Author

# Category

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorForm

    list_display = ["title", "identifier", "published", 'order_id', 'languages']
    inlines = (AuthorTranslationInline, )


    def title(self, obj):
        return '%s %s' % (obj.first_name, obj.last_name)

    def languages(self, obj):
        ts=[]
        for t in obj.get_translations():
            ts.append(u'<img src="/static/admin/img/flags/%s.png" alt="" rel="tooltip" data-title="%s">' % (t.language_code, t.__unicode__()))
        return ' '.join(ts)

    languages.allow_tags = True
    languages.short_description = 'Translations'

    # Override the list display from PublishingWorkflowAdmin
    def get_list_display(self, request, obj=None):
        if not settings.PREFIX_DEFAULT_LOCALE:
            return ["title", "identifier", "published", 'order_id']
        else:
            return ["title", "identifier", "published", 'order_id', 'languages']

    fieldsets = (

        
        ('Settings', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('published', 'first_name', 'last_name', 'photo', 'order_id', 'identifier', )
        }),

    )

    class Media:
        css = {
            "all": ("admin/css/page.css",)
        }
        #js = ("admin/js/page.js",)

admin.site.register(Author, AuthorAdmin)