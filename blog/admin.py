import reversion

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.admin.views.main import ChangeList

from mptt.admin import MPTTModelAdmin
from multilingual_model.admin import TranslationInline

from redactor.widgets import RedactorEditor

from cmsbase.admin import PageAdmin, PageFormAdmin, PublishingWorkflowAdmin
from cmsbase.widgets import AdminImageWidget, AdminCustomFileWidget

from blog.models import *

from filemanager.widgets import MultipleFileWidget

# Article translation

class ArticleTranslationInlineFormAdmin(forms.ModelForm):
    slug = forms.SlugField(label=_('Article URL'))
    content = forms.CharField(widget=RedactorEditor(redactor_css="/static/css/redactor-editor.css"), required=False)
    images = forms.CharField(widget=MultipleFileWidget, required=False)
    class Meta:
        model = ArticleTranslation

    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will get validated and saved."""
        return True

    def __init__(self, *args, **kwargs):
        from django.contrib.contenttypes.models import ContentType
        super(ArticleTranslationInlineFormAdmin, self).__init__(*args, **kwargs)

        if self.instance:
            content_type = ContentType.objects.get_for_model(self.instance)
            object_pk = self.instance.id
            self.fields['images'].widget.attrs.update({'content_type':content_type.id, 'object_pk':object_pk})
        else:
            self.fields['images'].widget.attrs.update({'content_type':False, 'object_pk':False})

class ArticleTranslationInline(TranslationInline):
    model = ArticleTranslation
    form = ArticleTranslationInlineFormAdmin
    extra = 0 if settings.PREFIX_DEFAULT_LOCALE else 1
    prepopulated_fields = {'slug': ('title',)}
    template = 'admin/cmsbase/cms_translation_inline.html'


# Article feature images

# class ImageInlineForm(forms.ModelForm):
#   image = forms.ImageField(label=_('Image'), widget=AdminImageWidget)
#   class Meta:
#       model=ArticleImage

# class ArticleImageInline(admin.TabularInline):
#   form = ImageInlineForm
#   model = ArticleImage
#   extra = 0
#   template = 'admin/cmsbase/page/images-inline.html'


# Article

class ArticleAdminForm(PageFormAdmin):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(), widget=forms.CheckboxSelectMultiple, required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.filter(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Article

class ArticleAdmin(reversion.VersionAdmin, PublishingWorkflowAdmin):
    form = ArticleAdminForm
    
    inlines = (ArticleTranslationInline, ) #, ArticleImageInline
    ordering = ['-publish_date'] 

    # Override the list display from PublishingWorkflowAdmin
    def get_list_display(self, request, obj=None):
        if not settings.PREFIX_DEFAULT_LOCALE:
            return ['title', 'is_published', 'approval', 'publish_date', 'template']
        else:
            return ['title', 'is_published', 'approval', 'publish_date', 'template', 'languages']

    fieldsets = (
        ('Settings', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('template', 'publish_date', 'slug',)
        }),
        ('Authors', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('authors',)
        }),
        ('Categories', {
            #'description':_('The page template'),
            'classes': ('default',),
            'fields': ('categories',)
        }),
        
    )

    class Media:
        css = {
            "all": ("admin/css/page.css",)
        }
        js = ("admin/js/page.js",)

admin.site.register(Article, ArticleAdmin)





# Category translation

class CategoryTranslationInline(TranslationInline):
    model = CategoryTranslation
    extra = 0 if settings.PREFIX_DEFAULT_LOCALE else 1
    prepopulated_fields = {'slug': ('title',)}
    template = 'admin/cmsbase/cms_translation_inline.html'



# Category

class CategoryAdmin(MPTTModelAdmin):

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

admin.site.register(Category, CategoryAdmin)


# Author translation

class AuthorTranslationInline(TranslationInline):
    model = AuthorTranslation
    extra = 0 if settings.PREFIX_DEFAULT_LOCALE else 1
    template = 'admin/cmsbase/cms_translation_inline.html'

class AuthorForm(forms.ModelForm):
    photo = forms.ImageField(label=_('Photo'), widget=AdminImageWidget)
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