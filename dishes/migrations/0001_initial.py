# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 11:52
from __future__ import unicode_literals

import dishes.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug for category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categoriess',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=dishes.models.upload_location, verbose_name='Image', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('preparing_time', models.TimeField()),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('for_vegan', models.BooleanField(default=False)),
                ('slug', models.SlugField(verbose_name='Slug for dish')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.Category')),
            ],
            options={
                'verbose_name': 'Dish',
                'verbose_name_plural': 'Dishes',
            },
        ),
    ]
