# Generated by Django 4.2.6 on 2023-10-18 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]