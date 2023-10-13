# Generated by Django 4.2.5 on 2023-10-13 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0010_rename_user_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Reviews'},
        ),
        migrations.RemoveField(
            model_name='review',
            name='date',
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]