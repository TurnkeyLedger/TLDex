# Generated by Django 2.1.7 on 2019-03-26 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0003_depositmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositmodel',
            name='success_boolean',
        ),
    ]
