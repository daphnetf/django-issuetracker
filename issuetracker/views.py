from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from issuetracker.mixins import LoginRequiredMixin
from issuetracker.models import Issue, IssueAction, IssueTag, Tag



class HomeView(TemplateView):

    template_name = 'issuetracker/home.html'


class IssueListView(ListView):

    model = Issue
    paginate_by = 10


class IssueCreateView(LoginRequiredMixin, CreateView):

    model = Issue
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super(IssueCreateView, self).form_valid(form)


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
