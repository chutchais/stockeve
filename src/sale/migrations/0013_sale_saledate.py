# Generated by Django 3.1.1 on 2020-10-29 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0012_auto_20200929_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='saledate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
