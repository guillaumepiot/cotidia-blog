from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

from cotidia.cms.models import (
    BasePage,
    BasePageTranslation,
    BasePageManager
)

from cotidia.blog import settings as blog_settings


class ArticleManager(BasePageManager):
    def get_published_live(self):
        return self.model.objects.filter(
            published=True, publish_date__lte=now()
        ).exclude(published_from=None)

    def get_published_translation_live(self, language_code=False):
        translation_model = self.model.CMSMeta.translation_class
        if language_code:
            return translation_model.objects.filter(
                parent__published=True,
                parent__publish_date__lte=now(),
                language_code=language_code
            ).exclude(parent__published_from=None)
        else:
            return translation_model.objects.filter(
                parent__published=True,
                parent__publish_date__lte=now()
            ).exclude(parent__published_from=None)


class ArticleTranslation(BasePageTranslation):
    parent = models.ForeignKey(
        'Article',
        related_name='translations',
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        'account.User',
        blank=True,
        null=True,
        related_name='article_translation_created_by',
        on_delete=models.SET_NULL
    )

    updated_by = models.ForeignKey(
        'account.User',
        blank=True,
        null=True,
        related_name='article_translation_updated_by',
        on_delete=models.SET_NULL
    )


class Article(BasePage):
    publish_date = models.DateTimeField(null=True)
    author = models.ForeignKey(
        'account.User',
        null=True,
        on_delete=models.SET_NULL
    )

    created_by = models.ForeignKey(
        'account.User',
        blank=True,
        null=True,
        related_name='article_created_by',
        on_delete=models.SET_NULL
    )

    updated_by = models.ForeignKey(
        'account.User',
        blank=True,
        null=True,
        related_name='articleupdated_by',
        on_delete=models.SET_NULL
    )

    objects = ArticleManager()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-publish_date']

    class CMSMeta:

        # Add a custom permission to publish an article
        permissions = (
            ("can_publish_article", "Can publish article"),
        )

        # A tuple of templates paths and names
        templates = blog_settings.BLOG_TEMPLATES

        # Indicate which Translation class to use for content
        translation_class = ArticleTranslation

        model_url_name = 'blog-public:article'
        admin_url_name = 'blog-admin:article-detail'

    def get_absolute_url(self, *args, **kwargs):
        if self.publish_date:
            year = self.publish_date.year
            month = self.publish_date.month
            day = self.publish_date.day
        else:
            year = self.date_created.year
            month = self.date_created.month
            day = self.date_created.day
        return super(Article, self).get_absolute_url(
            urlargs={'year': year, 'month': month, 'day': day},
            *args,
            **kwargs)

    def is_published(self):
        return self.publish_date <= now()

    @property
    def get_template(self):
        return dict(blog_settings.BLOG_TEMPLATES).get(self.template)


@receiver(post_save, sender=Article)
def update_article(sender, instance, **kwargs):
    if not instance.publish_date:
        instance.publish_date = instance.date_created
