# Generated by Django 2.2.7 on 2020-09-13 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0016_auto_20200913_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionmodel',
            options={'ordering': ['-date_at']},
        ),
        migrations.RenameField(
            model_name='answermodel',
            old_name='date',
            new_name='date_at',
        ),
        migrations.RenameField(
            model_name='questionmodel',
            old_name='date',
            new_name='date_at',
        ),
    ]
