# Generated by Django 2.1.7 on 2019-03-26 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0006_depositmodel_success_boolean'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositmodel',
            name='crypto_amount',
            field=models.FloatField(default=0.0),
        ),
    ]
