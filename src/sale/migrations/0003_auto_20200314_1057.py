# Generated by Django 2.2.7 on 2020-03-14 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_auto_20200314_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
