# Generated by Django 4.1.2 on 2022-12-03 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browserapp', '0003_usergames'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='games',
            name='coverBanner',
        ),
    ]