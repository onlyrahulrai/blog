# Generated by Django 3.1.3 on 2020-12-10 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='views',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
