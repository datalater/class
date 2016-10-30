# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='kakao_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_key', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(max_length=20, unique=True, verbose_name='학수번호')),
                ('major', models.CharField(max_length=30, verbose_name='전공')),
                ('lecture_name', models.CharField(max_length=30, verbose_name='강의 이름')),
                ('professor_name', models.CharField(max_length=30, verbose_name='교수 이름')),
                ('opening', models.IntegerField(verbose_name='여석')),
                ('total_number', models.IntegerField(verbose_name='자리')),
                ('popularity', models.IntegerField(default=0, verbose_name='조회 횟수')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
        ),
    ]
