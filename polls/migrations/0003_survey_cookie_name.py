# Generated by Django 2.1.7 on 2019-03-26 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20190325_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='cookie_name',
            field=models.CharField(default='x', max_length=20),
            preserve_default=False,
        ),
    ]
