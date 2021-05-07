# Generated by Django 3.2 on 2021-05-03 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_systemparameter_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemparameter',
            name='key',
            field=models.CharField(choices=[('SESSION_EXPIRATION_DATE_IN_SECONDS', 'SESSION_EXPIRATION_DATE_IN_SECONDS')], max_length=100, primary_key=True, serialize=False),
        ),
    ]
