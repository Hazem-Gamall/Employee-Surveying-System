# Generated by Django 4.1 on 2022-09-07 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey_system', '0004_alter_survey_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='quetion',
            new_name='question',
        ),
    ]