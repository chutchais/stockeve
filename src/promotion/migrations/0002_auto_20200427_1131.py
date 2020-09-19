# Generated by Django 3.0.2 on 2020-04-27 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_higher_stock'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotion',
            old_name='promotion_img',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='promotion',
            old_name='promotion_name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='promotion_detail',
        ),
        migrations.AddField(
            model_name='promotion',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promotion',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='enddate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promotions', to='product.Product'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='startdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
