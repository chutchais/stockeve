# Generated by Django 3.1.1 on 2020-09-28 03:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0009_soinvhd'),
    ]

    operations = [
        migrations.AddField(
            model_name='soinvhd',
            name='executed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='SoInvDT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listno', models.IntegerField()),
                ('goodid', models.IntegerField()),
                ('goodname', models.CharField(blank=True, max_length=200, null=True)),
                ('goodqty', models.IntegerField(default=1)),
                ('goodamnt', models.FloatField(default=0)),
                ('totalexcludeamnt', models.FloatField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('executed', models.BooleanField(default=False)),
                ('soinvid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sale.soinvhd')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('listno', 'soinvid')},
            },
        ),
    ]
