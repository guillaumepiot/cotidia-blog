# Generated by Django 2.0.1 on 2019-06-02 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_unique_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-publish_date'], 'permissions': (('publish_article', 'Can publish article'),), 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.RenameField(
            model_name='articletranslation',
            old_name='created_at',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='articletranslation',
            old_name='modified_at',
            new_name='date_updated',
        ),
        migrations.RemoveField(
            model_name='articletranslation',
            name='uuid',
        ),
    ]