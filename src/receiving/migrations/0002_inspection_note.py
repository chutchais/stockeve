# Generated by Django 2.2.7 on 2020-03-06 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiving', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='note',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]