# Generated by Django 2.1.7 on 2019-03-27 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0008_depositmodel_payment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositmodel',
            name='crypto_amount',
        ),
        migrations.RemoveField(
            model_name='depositmodel',
            name='payment_date',
        ),
    ]
