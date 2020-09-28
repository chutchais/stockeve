# Generated by Django 3.1.1 on 2020-09-27 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0008_auto_20200909_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoInvHD',
            fields=[
                ('soinvid', models.IntegerField(primary_key=True, serialize=False)),
                ('docuno', models.CharField(blank=True, max_length=50, null=True)),
                ('totabaseamnt', models.FloatField(default=0)),
                ('vatamnt', models.FloatField(default=0)),
                ('netamnt', models.FloatField(default=0)),
                ('saledate', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]