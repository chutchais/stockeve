# Generated by Django 3.0.4 on 2020-06-16 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_auto_20200519_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleChildDetail',
            fields=[
            ],
            options={
                'verbose_name': 'Child Product Sale Summary',
                'verbose_name_plural': 'Child Product Sales Summary',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sale.sale',),
        ),
    ]