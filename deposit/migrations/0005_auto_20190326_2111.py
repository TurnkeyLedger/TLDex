# Generated by Django 2.1.7 on 2019-03-26 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0004_remove_depositmodel_success_boolean'),
    ]

    operations = [
        migrations.RenameField(
            model_name='depositmodel',
            old_name='Crypto_Address',
            new_name='crypto_Address',
        ),
    ]
