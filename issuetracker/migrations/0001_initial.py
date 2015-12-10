# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('closed', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=256)),
                ('description', django_markdown.models.MarkdownField()),
                ('assignee', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='assignee')),
            ],
        ),
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('action', models.CharField(max_length=256)),
                ('icon', models.CharField(default='pencil', max_length=256)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('developers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('color', models.CharField(max_length=6)),
                ('project', models.ForeignKey(to='issuetracker.Project')),
            ],
        ),
        migrations.CreateModel(
            name='IssueAttachement',
            fields=[
                ('issueaction_ptr', models.OneToOneField(primary_key=True, to='issuetracker.IssueAction', auto_created=True, serialize=False, parent_link=True)),
                ('file', models.FileField(upload_to='')),
            ],
            bases=('issuetracker.issueaction',),
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('issueaction_ptr', models.OneToOneField(primary_key=True, to='issuetracker.IssueAction', auto_created=True, serialize=False, parent_link=True)),
                ('text', django_markdown.models.MarkdownField()),
            ],
            bases=('issuetracker.issueaction',),
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
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(to='issuetracker.Project'),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(related_name='repoter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(to='issuetracker.Tag', blank=True),
        ),
        migrations.AlterOrderWithRespectTo(
            name='issueaction',
            order_with_respect_to='issue',
        ),
    ]
