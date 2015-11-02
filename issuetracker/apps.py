from django.apps import AppConfig, apps
from django.db.models.signals import pre_save, post_save, m2m_changed

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


def issue_tags_changed(sender, instance, action, model, pk_set, using, **kwargs):
    """print('>>')
    print(sender)
    print(instance)
    print(action)
    print(model)
    print(pk_set)
    print(using)
    print('<<')"""


class IssuetrackerAppConfig(AppConfig):

    name = 'issuetracker'
    label = 'issuetracker'
    verbose_name = 'Issue Tracker'
    def ready(self):
        m2m_changed.connect(
            issue_tags_changed,
            sender=self.get_model('Issue').tags.through,
            dispatch_uid="tags_change"
        )
        post_save.connect(
            issue_created,
            sender=self.get_model('Issue')
        )
