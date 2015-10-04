from django.apps import AppConfig
from django.db.models.signals import post_save

def issue_created(sender, **kwargs):
    if kwargs['created'] == True:
        instance = kwargs['instance']
        ia = sender.get_model('IssueAction').objects.create(
            issue=instance,
            user=reporter,
            action=sender.get_model('IssueState').NEW
        )
        ia.save()
        if instance.assignee:
            instance.assign(reporter, instance.assignee)


class IssuetrackerAppConfig(AppConfig):

    name = 'issuetracker'
    verbose_name = 'Issue Tracker'
    def ready(self):
        post_save.connect(issue_created, sender=self.get_model('Issue'))