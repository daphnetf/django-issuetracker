from django.conf import settings
from django.db import models
from django_fsm import FSMField, transition
from django_markdown.models import MarkdownField
from issuetracker.middleware import get_current_user


class Tag(models.Model):
    name = models.CharField(max_length=256)
    colour = models.CharField(max_length=6)


class IssueState:
    NEW = 'new'
    UNASSIGNED = 'unassinged'
    ASSIGNED = 'assigned'
    CLOSED = 'closed'
    CHOICES = [NEW, UNASSIGNED, ASSIGNED, CLOSED]


class Issue(models.Model):
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=256)
    state = FSMField(
        default=IssueState.NEW,
        verbose_name='IssueState',
        choices=IssueState.CHOICES,
        protected=True,
    )

    @transition(field=state, source=[IssueState.NEW, IssueState.UNASSIGNED],
    target=IssueState.ASSIGNED)
    def assign(self, user):
        self.assignee = user
        IssueAction.objects.create(
            issue=self,
            action=IssueState.ASSIGNED
        ).save()

    @transition(field=state, source=[IssueState.ASSIGNED],
    target=IssueState.UNASSIGNED)
    def unassing(self):
        self.assignee = None
        IssueAction.objects.create(
            issue=self,
            action=IssueState.UNASSIGNED
        ).save()

    @transition(field=state, source=[IssueState.ASSIGNED],
    target=IssueState.CLOSED)
    def close(self):
        IssueAction.objects.create(
            issue=self,
            action=IssueState.CLOSED
        ).save()


class IssueAction(models.Model):
    issue = models.ForeignKey('issuetracker.Issue')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user)
    action = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)


class Comment(IssueAction):
    text = MarkdownField()


class IssueTag(models.Model):
    issue = models.ForeignKey('issuetracker.Issue')
    tag = models.ForeignKey('issuetracker.Tag')
