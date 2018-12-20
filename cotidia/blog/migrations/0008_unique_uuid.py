# Generated by Django 2.0.2 on 2018-12-04 12:54

from django.db import migrations, models
import uuid


def generate_uuid(apps, schema_editor):
    ArticleTranslation = apps.get_model("blog", "ArticleTranslation")

    for item in ArticleTranslation.objects.all():
        item.uuid = uuid.uuid4()
        item.save()


def dummy(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("blog", "0007_auto_20181220_1304")]

    operations = [
        migrations.RunPython(generate_uuid, dummy),
        migrations.AlterField(
            model_name="articletranslation",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
