# Generated by Django 3.2 on 2021-05-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210502_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='bla', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_eng',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_est',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_rus',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
