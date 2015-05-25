# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('weight', models.IntegerField(default=0, help_text=b'Peso da Historia dentro do Projeto para o Product Owner', null=True, blank=True)),
                ('priority', models.IntegerField(default=0, help_text=b'Prioridade da hist\xc3\xb3ria.', null=True, blank=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
                ('created_by', models.ForeignKey(verbose_name=b'Created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historia',
                'verbose_name_plural': 'Historias',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
                ('created_by', models.ForeignKey(verbose_name=b'Created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organizacao',
                'verbose_name_plural': 'Organizacoes',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Project')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
                ('created_by', models.ForeignKey(verbose_name=b'Created by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='core.Organization', null=True)),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('start_at', models.DateField(default=datetime.datetime(2015, 5, 25, 13, 53, 1, 826085), null=True, verbose_name=b'Start at')),
                ('end_at', models.DateField(default=datetime.datetime(2015, 6, 9, 13, 53, 1, 826118), verbose_name=b'End at', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
                ('created_by', models.ForeignKey(verbose_name=b'Created by', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='core.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(default=b'F', max_length=1, choices=[(b'F', b'Feature'), (b'R', b'Refatoracao'), (b'T', b'Teste'), (b'C', b'Correcao')])),
                ('weight', models.IntegerField(help_text=b'Peso da Tarefa dentro da historia para o Team', null=True, blank=True)),
                ('priority', models.IntegerField(default=0, help_text=b'Prioridade da tarefa.', null=True, blank=True)),
                ('estimate', models.CharField(default=b'?', max_length=3, choices=[(b'0.5', b'0.5'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5'), (b'8', b'8'), (b'13', b'13'), (b'20', b'20'), (b'40', b'40'), (b'100', b'100'), (b'INF', b'Infinito'), (b'?', b'?')])),
                ('status', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Nova'), (b'2', b'Andamento'), (b'3', b'Revisando'), (b'4', b'Completa')])),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
                ('associated_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Associated at')),
                ('associated_to', models.ForeignKey(related_name='associated_to', verbose_name=b'Associated to', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('created_by', models.ForeignKey(related_name='created_by', verbose_name=b'Created by', to=settings.AUTH_USER_MODEL)),
                ('history', models.ForeignKey(to='core.History')),
            ],
            options={
                'verbose_name': 'Tarefa',
                'verbose_name_plural': 'Tarefas',
            },
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='core.Task')),
            ],
        ),
        migrations.CreateModel(
            name='WorkHour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField(default=datetime.date(2015, 5, 25))),
                ('time', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(to='core.Task')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Horas de Trabalho',
                'verbose_name_plural': 'Horas de Trabalho',
            },
        ),
        migrations.AddField(
            model_name='history',
            name='project',
            field=models.ForeignKey(to='core.Project'),
        ),
        migrations.AddField(
            model_name='history',
            name='sprint',
            field=models.ForeignKey(blank=True, to='core.Sprint', null=True),
        ),
    ]
