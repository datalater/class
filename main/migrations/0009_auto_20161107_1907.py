# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_major_list_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='major_list',
            name='major_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
