# Generated by Django 4.2.5 on 2023-10-10 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_alter_books_rating_alter_users_favorite_books_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='generos',
            new_name='genres',
        ),
    ]
