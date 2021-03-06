# Generated by Django 2.2.5 on 2020-02-07 08:49

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_remove_postview_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, default='slug', editable=False, populate_from='title'),
            preserve_default=False,
        ),
    ]
