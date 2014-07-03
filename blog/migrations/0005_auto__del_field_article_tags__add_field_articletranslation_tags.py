# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.tags'
        db.delete_column(u'blog_article', 'tags')

        # Adding field 'ArticleTranslation.tags'
        db.add_column(u'blog_articletranslation', 'tags',
                      self.gf('tagging_autocomplete.models.TagAutocompleteField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Article.tags'
        db.add_column(u'blog_article', 'tags',
                      self.gf('tagging_autocomplete.models.TagAutocompleteField')(default=''),
                      keep_default=False)

        # Deleting field 'ArticleTranslation.tags'
        db.delete_column(u'blog_articletranslation', 'tags')


    models = {
        u'blog.article': {
            'Meta': {'ordering': "['-publish_date']", 'object_name': 'Article'},
            'approval_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Author']", 'symmetrical': 'False', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'to': u"orm['blog.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.ArticleDataSet']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'display_title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'hide_from_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blog.Article']"}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Article']", 'null': 'True', 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'redirect_to_page'", 'null': 'True', 'to': u"orm['blog.Article']"}),
            'redirect_to_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'related_pages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_pages_rel_+'", 'blank': 'True', 'to': u"orm['blog.Article']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'default': "'_self'", 'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'cms/page.html'", 'max_length': '250'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'blog.articledataset': {
            'Meta': {'object_name': 'ArticleDataSet'},
            'config': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.articletranslation': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'ArticleTranslation'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['blog.Article']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'blog.author': {
            'Meta': {'ordering': "['order_id']", 'object_name': 'Author'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {})
        },
        u'blog.authortranslation': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'AuthorTranslation'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['blog.Author']"})
        },
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blog.Category']"}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'blog.categorytranslation': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'CategoryTranslation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['blog.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blog']