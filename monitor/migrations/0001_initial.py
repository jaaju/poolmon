# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-04 07:34
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import monitor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Give a name for the pool.', max_length=50, unique=True)),
                ('depth', models.DecimalField(decimal_places=2, help_text='Max. depth (ft.)', max_digits=4)),
                ('area', models.DecimalField(decimal_places=2, help_text='Surface area (sq. ft.)', max_digits=6)),
                ('size', models.IntegerField(help_text='Pool volume (gallons)')),
                ('fill_rate', models.IntegerField(help_text='# times/week the pool is filled.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('covered', models.BooleanField(help_text='Is the pool covered?')),
            ],
        ),
        migrations.CreateModel(
            name='PoolOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PoolReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('level', models.IntegerField(choices=[(monitor.models.PoolLevel(1), 'Good'), (monitor.models.PoolLevel(0), 'Bad')], default=monitor.models.PoolLevel(1))),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pool', to='monitor.Pool')),
            ],
        ),
        migrations.AddField(
            model_name='pool',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.PoolOwner'),
        ),
    ]
