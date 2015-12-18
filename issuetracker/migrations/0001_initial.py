# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('closed', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('assignee', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='assignee', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('action', models.CharField(max_length=256)),
                ('icon', models.CharField(max_length=256, default='pencil')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('developers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('color', models.CharField(max_length=6)),
                ('project', models.ForeignKey(to='issuetracker.Project')),
            ],
        ),
        migrations.CreateModel(
            name='IssueAttachement',
            fields=[
                ('issueaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, to='issuetracker.IssueAction', serialize=False)),
                ('file', models.FileField(upload_to='')),
            ],
            bases=('issuetracker.issueaction',),
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('issueaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, to='issuetracker.IssueAction', serialize=False)),
                ('text', models.TextField()),
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
