# Generated by Django 2.1.7 on 2019-09-05 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20190701_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Survey')),
            ],
        ),
    ]