# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('manager_name', models.CharField(max_length=20)),
                ('manager_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('school_name', models.CharField(max_length=20)),
                ('school_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='manager',
            name='my_school',
            field=models.OneToOneField(to='rlt_db.School'),
        ),
    ]
