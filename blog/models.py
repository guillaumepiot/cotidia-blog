from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings

from multilingual_model.models import MultilingualModel, MultilingualTranslation
from cmsbase.models import BasePage, PublishTranslation




# Subclass the PageTranslation model to create the article translation

class ArticleTranslation(MultilingualTranslation, PublishTranslation):
	parent = models.ForeignKey('Article', related_name='translations')
	title = models.CharField(_('Article title'), max_length=100)
	slug = models.SlugField(max_length=60)
	content = models.TextField(blank=True)

	#Meta data
	meta_title = models.CharField(max_length=100, blank=True)
	meta_description = models.TextField(blank=True)

	class Meta:
		unique_together = ('parent', 'language_code')

		if len(settings.LANGUAGES) > 1:
			verbose_name=_('Translation')
			verbose_name_plural=_('Translations')
		else:
			verbose_name=_('Content')
			verbose_name_plural=_('Content')

	def __unicode__(self):
		return dict(settings.LANGUAGES).get(self.language_code)


class ArticleManager(models.Manager):

    def get_published_live(self):
        return Article.objects.filter(published=True).exclude(published_from=None)

    def get_published_original(self):
        return Article.objects.filter(published=True, published_from=None)

    def get_originals(self):
        return Article.objects.filter(published_from=None)

# Subclass the Page model to create the article model

class Article(BasePage):
	# Extra fields
	publish_date = models.DateTimeField()

	# Manager
	objects = ArticleManager()

	# Indicate which Translation class to use for content
	translation_class = ArticleTranslation

	class Meta:
		verbose_name=_('Article')
		verbose_name_plural=_('Articles')

		
