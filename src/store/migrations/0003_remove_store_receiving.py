# Generated by Django 2.2.7 on 2020-03-05 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_receiving'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='receiving',
        ),
    ]