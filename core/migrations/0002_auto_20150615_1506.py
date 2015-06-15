# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Em espera'), (1, b'Executando'), (2, b'Completa'), (3, b'Cancelada')]),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='end_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 30, 15, 6, 12, 784258), verbose_name=b'End at', blank=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='start_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 15, 15, 6, 12, 784211), null=True, verbose_name=b'Start at'),
        ),
        migrations.AlterField(
            model_name='workhour',
            name='day',
            field=models.DateField(default=datetime.date(2015, 6, 15)),
        ),
    ]
