import reversion
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from localeurl.models import reverse

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from multilingual_model.models import MultilingualModel, MultilingualTranslation
from cmsbase.models import BasePage, BaseDataSet, BasePageTranslation, BasePageManager

from filemanager.models import FileToObject

from blog import settings as blog_settings

try:
    from tagging_autocomplete.models import TagAutocompleteField
except:
    TagAutocompleteField = models.CharField

class ArticleDataSet(BaseDataSet):

    class Meta:
        verbose_name=_('Article data set')
        verbose_name_plural=_('Article data sets')

# Subclass the PageTranslation model to create the article translation

class ArticleTranslation(BasePageTranslation):
    parent = models.ForeignKey('Article', related_name='translations')
    # Tagging
    tags = TagAutocompleteField()

    # TAGS
    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def add_tag(self, tag):
        Tag.objects.add_tag(self, tag)

    def related_tags(self):
        '''Tags of items that have all of the Tags'''
        return Tag.objects.related_for_model(self.tags, self.__class__, counts=True)

    def get_cloud(self):
        '''The raw list of tags with count and font_size attributes'''
        return Tag.objects.cloud_for_model(self.__class__)

    def render_cloud(self):
        '''Produce the html for the cloud'''
        context = { 'tags': self.get_cloud(), }
        return render_node(tag_cloud_template, context)

    def related_translations(self, num=None):
        '''Instances of this model that have a tag in common'''
        return TaggedItem.objects.get_related(self, self.__class__, num=num)

    def translations_common_tag(self):
        '''Same as related_attractions but with a different method'''
        return TaggedItem.objects.get_union_by_model(
            self.__class__.objects.exclude(slug=self.slug),
            self.tags
        )

reversion.register(ArticleTranslation)

class ArticleManager(BasePageManager):
    def get_published_live(self):
        return self.model.objects.filter(published=True, publish_date__lte=now()).exclude(published_from=None)

    def get_published_translation_live(self, language_code=False):
        translation_model = self.model.CMSMeta.translation_class
        if language_code:
            return translation_model.objects.filter(parent__published=True, parent__publish_date__lte=now(), language_code=language_code).exclude(parent__published_from=None)
        else:
            return translation_model.objects.filter(parent__published=True, parent__publish_date__lte=now()).exclude(parent__published_from=None)


# Subclass the Page model to create the article model

# Make this field usable by django south
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

class Article(BasePage):
    #Page mask
    dataset = models.ForeignKey('ArticleDataSet', blank=True, null=True)
    # Extra fields
    publish_date = models.DateTimeField()
    categories = TreeManyToManyField('Category', blank=True)
    authors = models.ManyToManyField('Author', blank=True)
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

        # Provide the url name to create a url for that model
        model_url_name = 'blog:article'

    def get_absolute_url(self, *args, **kwargs):
        return super(Article, self).get_absolute_url(urlargs={'year':self.publish_date.year, 'month':self.publish_date.month, 'day':self.publish_date.day}, *args, **kwargs)

    # Method for images against translation
    # def images(self):
    #     from django.utils.translation import get_language

    #     images = []
    #     if self.published_from:
    #         # Get the the original translation in the right language
    #         translation = self.CMSMeta.translation_class.objects.get(language_code=get_language(), parent=self.published_from)
    #     else:
    #         # Get the the original translation in the right language
    #         translation = self.CMSMeta.translation_class.objects.get(language_code=get_language(), parent=self)
        
    #     images = FileToObject.objects.filter(content_type=ContentType.objects.get_for_model(translation), object_pk=translation.id, file__is_image=True).order_by('order_id')

    #     return images

    # Method for images against page itself
    def images(self):
        #from django.utils.translation import get_language
        if self.published_from:
            images = FileToObject.objects.filter(content_type=ContentType.objects.get_for_model(Article), object_pk=self.published_from.id, file__is_image=True).order_by('order_id')
        else:
            images = FileToObject.objects.filter(content_type=ContentType.objects.get_for_model(Article), object_pk=self.id, file__is_image=True).order_by('order_id')
        return images

    def feature_image(self):

        images = self.images()

        if images.count() > 0:
            return images[0]
        else:
            return False


reversion.register(Article, follow=["translations"])

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

    def article_count(self):
        return Article.objects.get_published_live().filter(published_from__categories=self.id).count()

# Blog categories

class AuthorTranslation(MultilingualTranslation):
    parent = models.ForeignKey('Author', related_name='translations')
    bio = models.TextField(_('Bio'), max_length=100)

    class Meta:
        unique_together = ('parent', 'language_code')

        if len(settings.LANGUAGES) > 1:
            verbose_name=_('Translation')
            verbose_name_plural=_('Translations')
        else:
            verbose_name=_('Bio')
            verbose_name_plural=_('Bio')

    def __unicode__(self):
        return dict(settings.LANGUAGES).get(self.language_code)

    

class Author(MultilingualModel):
    identifier = models.SlugField(max_length=100, blank=True)
    published = models.BooleanField(_('Active'))
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    photo = models.ImageField(_('Photo'), upload_to="author", blank=True)
    order_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name=_('Author')
        verbose_name_plural=_('Authors')
        ordering = ['order_id']

    class CMSMeta:
        translation_class = AuthorTranslation

    def __unicode__(self):
        return self.unicode_wrapper('first_name', default='Unnamed')

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
        return reverse('blog:author', kwargs={'slug':self.identifier})

    def article_count(self):
        return Article.objects.get_published_live().filter(published_from__authors=self.id).count()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)