# Generated by Django 2.1.7 on 2019-03-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0005_auto_20190326_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositmodel',
            name='success_boolean',
            field=models.BooleanField(default=False),
        ),
    ]
