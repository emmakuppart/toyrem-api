# Generated by Django 3.2 on 2021-05-03 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210503_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemparameter',
            name='description',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
