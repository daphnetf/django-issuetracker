# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('closed', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=256)),
                ('assignee', models.ForeignKey(blank=True, null=True, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(related_name='repoter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=256)),
                ('icon', models.CharField(default='pencil', max_length=256)),
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
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('color', models.CharField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(blank=True, to='issuetracker.Tag'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='issueaction',
            order_with_respect_to='issue',
        ),
    ]
