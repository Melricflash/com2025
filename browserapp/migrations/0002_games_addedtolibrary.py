# Generated by Django 4.1.2 on 2022-11-28 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browserapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='addedToLibrary',
            field=models.BooleanField(default=False),
        ),
    ]