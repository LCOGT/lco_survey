# Generated by Django 2.1.7 on 2019-03-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_survey_cookie_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='cookie_name',
            field=models.CharField(help_text="Should start 'lco_fb_'", max_length=20),
        ),
    ]