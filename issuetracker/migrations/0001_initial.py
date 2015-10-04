# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm
from django.conf import settings
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=256)),
                ('state', django_fsm.FSMField(max_length=50, default='new', verbose_name='IssueState', protected=True, choices=[('new', 'New'), ('unassinged', 'Unassigned'), ('assigned', 'Assigned'), ('closed', 'Closed')])),
                ('assignee', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='assignee')),
                ('reporter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='repoter')),
            ],
        ),
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('issue', models.ForeignKey(to='issuetracker.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
