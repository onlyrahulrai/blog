# Generated by Django 3.1.3 on 2020-12-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_comment_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='views',
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
