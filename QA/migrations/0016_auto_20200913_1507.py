# Generated by Django 2.2.7 on 2020-09-13 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0015_auto_20200913_0644'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answermodel',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='qtagmodel',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='answermodel',
            constraint=models.UniqueConstraint(fields=('question', 'author'), name='answer'),
        ),
        migrations.AddConstraint(
            model_name='qtagmodel',
            constraint=models.UniqueConstraint(fields=('question', 'tag'), name='qtag'),
        ),
    ]
