from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from itertools import chain


class Project(models.Model):
    name = models.CharField(
        max_length=256
    )
    developers = models.ManyToManyField(
        settings.AUTH_USER_MODEL
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('issuetracker:project', kwargs={'pk': self.pk})

    def can_edit(self, user):
        if self.developers.filter(username=user.username).exists():
            return True
        return False


class Tag(models.Model):
    name = models.CharField(
        max_length=256
    )
    color = models.CharField(
        max_length=6
    )
    project = models.ForeignKey(
        Project
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('issuetracker:tag', kwargs={'pk': self.pk})

    def can_edit(self, user):
        return self.project.can_edit(user)


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
    description = models.TextField(
    )
    project = models.ForeignKey(
        Project
    )

    def actions(self):
        attachements = IssueAttachement.objects.filter(issue=self)
        comments = IssueComment.objects.filter(issue=self)
        actions = IssueAction.objects.filter(issue=self).exclude(pk__in=attachements).exclude(pk__in=comments)
        return sorted(chain(actions, comments, attachements), key= lambda x: x.pk)

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
            icon='user',
            action=_('changed assignement to {assignee}'.format(assignee=assignee))
        )

    def unassign(self, user):
        self.assignee = None
        IssueAction.objects.create(
            issue=self,
            user=user,
            icon='pencil',
            action=_('removed assignement')
        )

    def close(self, user):
        self.closed = True
        IssueAction.objects.create(
            issue=self,
            user=user,
            icon='ok',
            action=_('closed')
        )

    def open(self, user):
        self.closed = False
        IssueAction.objects.create(
            issue=self,
            user=user,
            icon='plus',
            action=_('opened')
        )

    def changed(self, user, thing):
        IssueAction.objects.create(
            issue=self,
            user=user,
            icon='pencil',
            action=_('changed issue {thing}'.format(thing=thing))
        )

    def can_edit(self, user):
        if self.project.can_edit(user):
            return True
        if self.assignee == user:
            return True
        if self.reporter == user:
            return True
        return False

    def get_tags(self):
        return self.tags.all()


class IssueAction(models.Model):

    class Meta:
        get_latest_by = 'created'
        order_with_respect_to = 'issue'

    issue = models.ForeignKey(
        'issuetracker.Issue',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    action = models.CharField(
        max_length=256,
    )
    icon = models.CharField(
        max_length=256,
        default='pencil',
    )
    created = models.DateTimeField(
        editable=False,
        blank=True,
    )
    changed = models.DateTimeField(
        editable=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.pk:
            self.created = now
        self.changed = now
        super().save(*args, **kwargs)

    def is_changed(self):
        return self.created < self.changed

    def __str__(self):
        return self.action

    def get_success_url(self):
        return reverse_lazy('issuetracker:issue', kwargs={'pk': self.issue.pk})


class IssueComment(IssueAction):

    text = models.TextField(
    )


class IssueAttachement(IssueAction):

    file = models.FileField(
    )
