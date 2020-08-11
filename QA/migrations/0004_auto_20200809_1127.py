# Generated by Django 3.0.7 on 2020-08-09 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0003_auto_20200808_1408'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='qvote',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='qvote',
            constraint=models.UniqueConstraint(fields=('question', 'user'), name='qvote'),
        ),
    ]