# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from blog.models import Article


class Command(BaseCommand):
    args = ''
    help = 'Add the publish permission to the article model'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Article)
        Permission.objects.get_or_create(
            codename='publish_article',
            name='Can publish article',
            content_type=content_type
            )
