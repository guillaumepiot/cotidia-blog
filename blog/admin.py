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

from blog.models import *


# Article translation

class ArticleTranslationInlineFormAdmin(forms.ModelForm):
	slug = forms.SlugField(label=_('Article URL'))
	content = forms.CharField(widget=RedactorEditor(redactor_css="/static/css/redactor-editor.css"), required=False)

	class Meta:
		model = ArticleTranslation

	def has_changed(self):
		""" Should returns True if data differs from initial.
		By always returning true even unchanged inlines will get validated and saved."""
		return True

class ArticleTranslationInline(TranslationInline):
	model = ArticleTranslation
	form = ArticleTranslationInlineFormAdmin
	extra = 0 if settings.PREFIX_DEFAULT_LOCALE else 1
	prepopulated_fields = {'slug': ('title',)}
	template = 'admin/cmsbase/cms_translation_inline.html'



# Article

class ArticleAdminForm(PageFormAdmin):
	categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(), widget=forms.CheckboxSelectMultiple)
	class Meta:
		model = Article

class ArticleAdmin(reversion.VersionAdmin, PublishingWorkflowAdmin):
	form = ArticleAdminForm
	
	inlines = (ArticleTranslationInline, )
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
			'fields': ('template', 'publish_date', 'slug', 'categories')
		}),
	)

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