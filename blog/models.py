from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from localeurl.models import reverse

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from multilingual_model.models import MultilingualModel, MultilingualTranslation
from cmsbase.models import BasePage, PublishTranslation, BasePageManager


from blog import settings as blog_settings


# Subclass the PageTranslation model to create the article translation

class ArticleTranslation(MultilingualTranslation, PublishTranslation):
	parent = models.ForeignKey('Article', related_name='translations')
	title = models.CharField(_('Article title'), max_length=100)
	slug = models.SlugField(max_length=100)
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


class ArticleImage(models.Model):

	def call_naming(self, instance=None):
		from cmsbase.widgets import get_media_upload_to

		# return get_media_upload_to(self.page.slug, 'pages')
		location = "blog/%s/%s"%(self.parent.publish_date.year, self.parent.publish_date.month)
		return get_media_upload_to(location, instance)

	parent = models.ForeignKey('Article')
	image = models.ImageField(upload_to=call_naming, max_length=100)
	# Ordering
	order_id = models.IntegerField(blank=True, null=True)

	class Meta:
		ordering = ('order_id',)
		verbose_name = _('Image')
		verbose_name_plural = _('Images')

	def delete(self, *args, **kwargs):
		from sorl.thumbnail import get_thumbnail
		storage, path = self.image.storage, self.image.path
		super(ArticleImage, self).delete(*args, **kwargs)
		# Physically delete the file
		storage.delete(path)


class ArticleManager(BasePageManager):
	pass

# Subclass the Page model to create the article model

class Article(BasePage):
	# Extra fields
	publish_date = models.DateTimeField()
	categories = TreeManyToManyField('Category', blank=True)
	# Manager
	objects = ArticleManager()

	class Meta:
		verbose_name=_('Article')
		verbose_name_plural=_('Articles')
		ordering = ['-publish_date']

	class CMSMeta:
	
		# A tuple of templates paths and names
		templates = blog_settings.BLOG_TEMPLATES
		
		# Indicate which Translation class to use for content
		translation_class = ArticleTranslation
		image_class = ArticleImage

		# Provide the url name to create a url for that model
		model_url_name = 'blog:article'

		
# Blog categories

class CategoryTranslation(MultilingualTranslation):
	parent = models.ForeignKey('Category', related_name='translations')
	title = models.CharField(_('Category title'), max_length=100)
	slug = models.SlugField(max_length=100)

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

	

class Category(MPTTModel, MultilingualModel):
	#MPTT parent
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	identifier = models.SlugField(max_length=100)
	published = models.BooleanField(_('Active'))
	order_id = models.IntegerField()

	class Meta:
		verbose_name=_('Category')
		verbose_name_plural=_('Categories')

	class MPTTMeta:
		order_insertion_by = ['order_id']

	class CMSMeta:
		translation_class = CategoryTranslation

	def __unicode__(self):
		return self.unicode_wrapper('title', default='Unnamed')

	def get_translations(self):
		return self.CMSMeta.translation_class.objects.filter(parent=self)

	def translated(self):
		from django.utils.translation import get_language

		try:
			translation = self.CMSMeta.translation_class.objects.get(language_code=get_language(), parent=self)
			return translation
		except:
			return self.CMSMeta.translation_class.objects.get(language_code=settings.LANGUAGE_CODE, parent=self)

	def get_absolute_url(self):
		return reverse('blog:category', kwargs={'slug':self.translated().slug})