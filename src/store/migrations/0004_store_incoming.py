# Generated by Django 2.2.7 on 2020-03-14 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_store_receiving'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='incoming',
            field=models.BooleanField(default=False),
        ),
    ]
