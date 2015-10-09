# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models
import django_fsm
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('text', django_markdown.models.MarkdownField()),
                ('state', django_fsm.FSMField(choices=[('new', 'New'), ('unassinged', 'Unassigned'), ('assigned', 'Assigned'), ('closed', 'Closed')], protected=True, verbose_name='IssueState', default='new', max_length=50)),
                ('assignee', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='assignee', blank=True)),
                ('reporter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='repoter')),
            ],
        ),
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=256)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', django_markdown.models.MarkdownField()),
                ('issue', models.ForeignKey(to='issuetracker.Issue')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='IssueTag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('issue', models.ForeignKey(to='issuetracker.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('colour', models.CharField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='issuetag',
            name='tag',
            field=models.ForeignKey(to='issuetracker.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='issuetag',
            unique_together=set([('issue', 'tag')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='issueaction',
            order_with_respect_to='issue',
        ),
    ]
