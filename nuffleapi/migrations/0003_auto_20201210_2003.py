# Generated by Django 3.1.4 on 2020-12-10 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nuffleapi', '0002_remove_coach_leageadmin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='username',
            new_name='title',
        ),
    ]
