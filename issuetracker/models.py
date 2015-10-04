from django.conf import settings
from django.db import models
from django_fsm import FSMField, transition
from django_markdown.models import MarkdownField


class Tag(models.Model):
    name = models.CharField(
        max_length=256
    )
    colour = models.CharField(
        max_length=6
    )

    def __str__(self):
        return self.name


class IssueState:
    NEW = 'new'
    UNASSIGNED = 'unassinged'
    ASSIGNED = 'assigned'
    CLOSED = 'closed'
    CHOICES = [
        (NEW, 'New'),
        (UNASSIGNED, 'Unassigned'),
        (ASSIGNED, 'Assigned'),
        (CLOSED, 'Closed')
    ]


class Issue(models.Model):
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='assignee'
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='repoter'
    )
    title = models.CharField(
        max_length=256
    )
    state = FSMField(
        default=IssueState.NEW,
        verbose_name='IssueState',
        choices=IssueState.CHOICES,
        protected=True,
    )

    @transition(field=state, source=[IssueState.NEW, IssueState.UNASSIGNED],
    target=IssueState.ASSIGNED)
    def assign(self, user, assignee):
        self.assignee = assignee
        IssueAction.objects.create(
            issue=self,
            user=user,
            action=IssueState.ASSIGNED
        ).save()

    @transition(field=state, source=[IssueState.ASSIGNED],
    target=IssueState.UNASSIGNED)
    def unassing(self, uesr):
        self.assignee = None
        IssueAction.objects.create(
            issue=self,
            user=user,
            action=IssueState.UNASSIGNED
        ).save()

    @transition(field=state, source=[IssueState.ASSIGNED],
    target=IssueState.CLOSED)
    def close(self, user):
        IssueAction.objects.create(
            issue=self,
            user=user,
            action=IssueState.CLOSED
        ).save()


class IssueAction(models.Model):
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


class Comment(IssueAction):
    text = MarkdownField()


class IssueTag(models.Model):
    issue = models.ForeignKey(
        'issuetracker.Issue'
    )
    tag = models.ForeignKey(
        'issuetracker.Tag'
    )
