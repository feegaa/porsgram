# Generated by Django 2.2.7 on 2020-09-12 18:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0013_auto_20200912_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='answermodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
