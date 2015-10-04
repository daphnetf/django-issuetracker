from django.views.generic import ListView, TemplateView

from issuetracker.models import Issue, Tag


class HomeView(TemplateView):
    template_name = 'issuetracker/home.html'

class IssueListView(ListView):
    model = Issue
    paginate_by = 10

class TagListView(ListView):
    model = Tag
