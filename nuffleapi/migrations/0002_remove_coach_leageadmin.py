# Generated by Django 3.1.4 on 2020-12-09 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nuffleapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='leageAdmin',
        ),
    ]
