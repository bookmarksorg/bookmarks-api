# Generated by Django 4.2.5 on 2023-10-17 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0013_alter_comments_id_user_alter_discussion_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='rating',
        ),
    ]
