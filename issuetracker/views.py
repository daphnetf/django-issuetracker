from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView

from issuetracker.models import Issue, IssueAction, IssueTag, Tag


class HomeView(TemplateView):

    template_name = 'issuetracker/home.html'


class IssueListView(ListView):

    model = Issue
    paginate_by = 10


class IssueView(DetailView):

    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueView, self).get_context_data(**kwargs)
        context['actions'] = IssueAction.objects.filter(
            issue=context['object']
        )
        context['tags'] = IssueTag.objects.filter(
            issue=context['object']
        )
        return context


class TagListView(ListView):

    model = Tag
