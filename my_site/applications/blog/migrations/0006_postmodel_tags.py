# Generated by Django 5.2 on 2025-04-16 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_tagsmodel_alter_commentmodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='blog.tagsmodel'),
        ),
    ]
