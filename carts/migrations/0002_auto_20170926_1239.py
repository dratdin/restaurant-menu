# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ('-created_at',), 'verbose_name': 'cart', 'verbose_name_plural': 'carts'},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
