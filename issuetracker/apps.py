from django.apps import AppConfig
from django.db.models.signals import post_save
from issuetracker.models import IssueAction, IssueState

def issue_created(sender, **kwargs):
    if kwargs['created'] == True:
        instance = kwargs['instance']
        ia = IssueAction.objects.create(
            issue=instance,
            action=IssueState.NEW
        )
        ia.save()
        if instance.assignee:
            instance.assign(instance.assignee)


class IssuetrackerAppConfig(AppConfig):

    name = 'issuetracker'
    verbose_name = 'Issue Tracker'
    def ready(self):
        post_save.connect(issue_created, sender=self.get_model('Issue'))