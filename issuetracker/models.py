from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django_markdown.models import MarkdownField
from django_markdown.utils import markdown as _markdown


class Tag(models.Model):
    name = models.CharField(
        max_length=256
    )
    color = models.CharField(
        max_length=6
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('issuetracker:tag', kwargs={'pk': self.pk})


class Issue(models.Model):
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='assignee',
    )
    closed = models.BooleanField(
        default=False,
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='repoter',
    )
    title = models.CharField(
        max_length=256,
    )
    tags = models.ManyToManyField(
        'issuetracker.Tag',
        blank=True,
    )

    def assigned(self):
        return self.assignee != None

    def get_absolute_url(self):
        return reverse_lazy('issuetracker:issue', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def assign(self, user, assignee):
        self.assignee = assignee
        IssueAction.objects.create(
            issue=self,
            user=user,
            action='assigned'
        ).save()

    def unassign(self, user):
        self.assignee = None
        IssueAction.objects.create(
            issue=self,
            user=user,
            action='unassigned'
        ).save()

    def close(self, user):
        self.closed = True
        IssueAction.objects.create(
            issue=self,
            user=user,
            action='closed'
        ).save()

    def open(self, user):
        self.closed = False
        IssueAction.objects.create(
            issue=self,
            user=user,
            action='opened'
        ).save()


class IssueAction(models.Model):

    class Meta:
        get_latest_by = 'date'
        order_with_respect_to = 'issue'

    issue = models.ForeignKey(
        'issuetracker.Issue'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL
    )
    action = models.CharField(
        max_length=256
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    text = MarkdownField()

    def __str__(self):
        return self.action

    def get_success_url(self):
        return reverse_lazy('issuetracker:issue', kwargs={'pk': self.issue.pk})
