# Generated by Django 3.1.1 on 2020-09-18 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0002_commentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='comment',
            field=models.CharField(max_length=500),
        ),
    ]
