# Generated by Django 2.2.5 on 2020-02-01 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_postview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postview',
            name='user',
        ),
    ]
