# Generated by Django 4.0.4 on 2022-11-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_uploadimage_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadimage',
            name='image',
            field=models.ImageField(upload_to='users/%Y/%m/%d/'),
        ),
    ]
