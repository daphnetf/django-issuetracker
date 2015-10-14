from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from issuetracker.mixins import LoginRequiredMixin
from issuetracker.models import Issue, IssueAction, Tag



class HomeView(TemplateView):

    template_name = 'issuetracker/home.html'


class IssueListView(ListView):

    model = Issue
    paginate_by = 10


class IssueCreateView(LoginRequiredMixin, CreateView):

    model = Issue
    fields = ['title', 'tags']

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class IssueDetailView(DetailView):

    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actions'] = IssueAction.objects.filter(
            issue=context['object']
        )
        return context


class TagListView(ListView):

    model = Tag


class TagCreateView(LoginRequiredMixin, CreateView):

    model = Tag
    fields = ['name', 'color']


class TagDetailView(DetailView):

    model = Tag
