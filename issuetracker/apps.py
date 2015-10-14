from django.apps import AppConfig, apps
from django.db.models.signals import post_save

def issue_created(sender, **kwargs):
    if kwargs['created'] == True:
        instance = kwargs['instance']
        ia = apps.get_model('issuetracker', 'IssueAction').objects.create(
                issue=instance,
                user=instance.reporter,
                action='opened'
        )
        ia.save()
        if instance.assignee:
            instance.assign(instance.reporter, instance.assignee)


class IssuetrackerAppConfig(AppConfig):

    name = 'issuetracker'
    label = 'issuetracker'
    verbose_name = 'Issue Tracker'
    def ready(self):
        post_save.connect(issue_created, sender=self.get_model('Issue'))
