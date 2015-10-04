# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_fsm
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=256)),
                ('state', django_fsm.FSMField(verbose_name='IssueState', default='new', max_length=50, choices=[('new', 'New'), ('unassinged', 'Unassigned'), ('assigned', 'Assigned'), ('closed', 'Closed')], protected=True)),
                ('assignee', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='assignee', null=True)),
                ('reporter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='repoter')),
            ],
        ),
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action', models.CharField(max_length=256)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('issue', models.ForeignKey(to='issuetracker.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('colour', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('issueaction_ptr', models.OneToOneField(primary_key=True, to='issuetracker.IssueAction', serialize=False, parent_link=True, auto_created=True)),
                ('text', django_markdown.models.MarkdownField()),
            ],
            bases=('issuetracker.issueaction',),
        ),
        migrations.AddField(
            model_name='issuetag',
            name='tag',
            field=models.ForeignKey(to='issuetracker.Tag'),
        ),
        migrations.AddField(
            model_name='issueaction',
            name='issue',
            field=models.ForeignKey(to='issuetracker.Issue'),
        ),
        migrations.AddField(
            model_name='issueaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
