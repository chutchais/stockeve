# Generated by Django 3.0.4 on 2020-05-20 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_finished_goods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='parent',
        ),
        migrations.AddField(
            model_name='product',
            name='childs',
            field=models.ManyToManyField(blank=True, null=True, related_name='parents', to='product.Product'),
        ),
    ]
