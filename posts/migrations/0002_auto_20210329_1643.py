# Generated by Django 3.1 on 2021-03-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.URLField(blank=True),
        ),
    ]
