# Generated by Django 4.1 on 2023-10-25 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_gender_relationship'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='friens',
            new_name='friends',
        ),
    ]
