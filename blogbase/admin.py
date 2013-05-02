from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from multilingual_model.admin import TranslationInline

from redactor.widgets import RedactorEditor

from cmsbase.admin import PageAdmin, PageFormAdmin

from blogbase.models import Article, ArticleTranslation


# Translation

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
	class Meta:
		model = Article

class ArticleAdmin(PageAdmin):
	form = ArticleAdminForm

	list_display = ["title", "is_published", "approval", 'template', 'languages']

	inlines = (ArticleTranslationInline, )

	fieldsets = (

		
		('Settings', {
			#'description':_('The page template'),
			'classes': ('default',),
			'fields': ('template', 'publish_date', 'slug', )
		}),

	)

admin.site.register(Article, ArticleAdmin)