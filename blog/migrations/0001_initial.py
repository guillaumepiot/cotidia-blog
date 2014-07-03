# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticleDataSet'
        db.create_table(u'blog_articledataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('config', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'blog', ['ArticleDataSet'])

        # Adding model 'ArticleTranslation'
        db.create_table(u'blog_articletranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['blog.Article'])),
        ))
        db.send_create_signal(u'blog', ['ArticleTranslation'])

        # Adding unique constraint on 'ArticleTranslation', fields ['parent', 'language_code']
        db.create_unique(u'blog_articletranslation', ['parent_id', 'language_code'])

        # Adding model 'Article'
        db.create_table(u'blog_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approval_needed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template', self.gf('django.db.models.fields.CharField')(default='cms/page.html', max_length=250)),
            ('display_title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['blog.Article'])),
            ('published_from', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Article'], null=True, blank=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsbase.PageDataSet'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=60, null=True, blank=True)),
            ('order_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approve', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('redirect_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='redirect_to_page', null=True, to=orm['blog.Article'])),
            ('redirect_to_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(default='_self', max_length=50)),
            ('hide_from_nav', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'blog', ['Article'])

        # Adding M2M table for field related_pages on 'Article'
        m2m_table_name = db.shorten_name(u'blog_article_related_pages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_article', models.ForeignKey(orm[u'blog.article'], null=False)),
            ('to_article', models.ForeignKey(orm[u'blog.article'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_article_id', 'to_article_id'])

        # Adding M2M table for field categories on 'Article'
        m2m_table_name = db.shorten_name(u'blog_article_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'blog.article'], null=False)),
            ('category', models.ForeignKey(orm[u'blog.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'category_id'])

        # Adding M2M table for field authors on 'Article'
        m2m_table_name = db.shorten_name(u'blog_article_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'blog.article'], null=False)),
            ('author', models.ForeignKey(orm[u'blog.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'author_id'])

        # Adding model 'CategoryTranslation'
        db.create_table(u'blog_categorytranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['blog.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal(u'blog', ['CategoryTranslation'])

        # Adding unique constraint on 'CategoryTranslation', fields ['parent', 'language_code']
        db.create_unique(u'blog_categorytranslation', ['parent_id', 'language_code'])

        # Adding model 'Category'
        db.create_table(u'blog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['blog.Category'])),
            ('identifier', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
            ('order_id', self.gf('django.db.models.fields.IntegerField')()),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'blog', ['Category'])

        # Adding model 'AuthorTranslation'
        db.create_table(u'blog_authortranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['blog.Author'])),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal(u'blog', ['AuthorTranslation'])

        # Adding unique constraint on 'AuthorTranslation', fields ['parent', 'language_code']
        db.create_unique(u'blog_authortranslation', ['parent_id', 'language_code'])

        # Adding model 'Author'
        db.create_table(u'blog_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('order_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'blog', ['Author'])


    def backwards(self, orm):
        # Removing unique constraint on 'AuthorTranslation', fields ['parent', 'language_code']
        db.delete_unique(u'blog_authortranslation', ['parent_id', 'language_code'])

        # Removing unique constraint on 'CategoryTranslation', fields ['parent', 'language_code']
        db.delete_unique(u'blog_categorytranslation', ['parent_id', 'language_code'])

        # Removing unique constraint on 'ArticleTranslation', fields ['parent', 'language_code']
        db.delete_unique(u'blog_articletranslation', ['parent_id', 'language_code'])

        # Deleting model 'ArticleDataSet'
        db.delete_table(u'blog_articledataset')

        # Deleting model 'ArticleTranslation'
        db.delete_table(u'blog_articletranslation')

        # Deleting model 'Article'
        db.delete_table(u'blog_article')

        # Removing M2M table for field related_pages on 'Article'
        db.delete_table(db.shorten_name(u'blog_article_related_pages'))

        # Removing M2M table for field categories on 'Article'
        db.delete_table(db.shorten_name(u'blog_article_categories'))

        # Removing M2M table for field authors on 'Article'
        db.delete_table(db.shorten_name(u'blog_article_authors'))

        # Deleting model 'CategoryTranslation'
        db.delete_table(u'blog_categorytranslation')

        # Deleting model 'Category'
        db.delete_table(u'blog_category')

        # Deleting model 'AuthorTranslation'
        db.delete_table(u'blog_authortranslation')

        # Deleting model 'Author'
        db.delete_table(u'blog_author')


    models = {
        u'blog.article': {
            'Meta': {'ordering': "['-publish_date']", 'object_name': 'Article'},
            'approval_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Author']", 'symmetrical': 'False', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'to': u"orm['blog.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsbase.PageDataSet']", 'null': 'True', 'blank': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'blog.author': {
            'Meta': {'ordering': "['order_id']", 'object_name': 'Author'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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
        },
        u'cmsbase.pagedataset': {
            'Meta': {'object_name': 'PageDataSet'},
            'config': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['blog']