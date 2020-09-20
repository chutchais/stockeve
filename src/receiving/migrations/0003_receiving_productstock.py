# Generated by Django 2.2.7 on 2020-03-14 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200314_0819'),
        ('receiving', '0002_inspection_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiving',
            name='productstock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receivings', to='product.ProductStock'),
        ),
    ]