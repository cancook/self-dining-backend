# Generated by Django 4.2.3 on 2023-07-06 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0002_youtubeingredients'),
        ('search', '0002_rename_is_vaild_ingredients_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredients',
            name='youtube',
            field=models.ManyToManyField(to='youtube.youtube'),
        ),
    ]
