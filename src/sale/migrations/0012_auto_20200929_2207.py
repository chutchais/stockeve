# Generated by Django 3.1.1 on 2020-09-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0011_soinvdt_goodcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='soinvdt',
            name='invecode',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='soinvdt',
            name='inveid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='soinvdt',
            name='invename',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]