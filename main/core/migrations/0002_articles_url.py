# Generated by Django 3.0.8 on 2020-10-11 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='url',
            field=models.SlugField(default='lol', max_length=130),
        ),
    ]
