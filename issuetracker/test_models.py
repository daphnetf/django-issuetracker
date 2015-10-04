from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from issuetracker.models import Issue, IssueAction, IssueState

class IssueTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', email='email', password='pass')

    def test_issue_creation_creates_action(self):
        self.assertEqual(0, len(IssueAction.objects.all()))
        i = Issue()
        i.reporter = self.user
        i.title = "Test Issue"
        i.save()
        self.assertEqual(1, len(IssueAction.objects.all()))
        ia = IssueAction.objects.all()[0]
        self.assertEqual(i, ia.issue)
        self.assertEqual(IssueState.NEW, ia.action)


    def test_issue_creation_creates_actions(self):
        self.assertEqual(0, len(IssueAction.objects.all()))
        i = Issue()
        i.reporter = self.user
        i.assignee = self.user
        i.title = "Test Issue"
        i.save()
        self.assertEqual(2, len(IssueAction.objects.all()))
        ia = IssueAction.objects.all()[0]
        self.assertEqual(i, ia.issue)
        self.assertEqual(IssueState.NEW, ia.action)
        ia = IssueAction.objects.all()[1]
        self.assertEqual(i, ia.issue)
        self.assertEqual(IssueState.ASSIGNED, ia.action)
