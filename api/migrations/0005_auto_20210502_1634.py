# Generated by Django 3.2 on 2021-05-02 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210502_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description_eng',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_est',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_rus',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]