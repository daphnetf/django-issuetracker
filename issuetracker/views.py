from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, TemplateView, FormView, View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from issuetracker.forms import IssueCommentForm, SearchForm, \
    IssueModelForm, IssueMetaModelForm
from issuetracker.mixins import LoginRequiredMixin, IssueViewMixin, \
    ProjectViewMixin, PreviewFormMixin
from issuetracker.models import Project, Issue, IssueAction, \
    IssueComment, IssueAttachement, Tag



class HomeView(TemplateView):

    template_name = 'issuetracker/home.html'


class ProjectListView(ProjectViewMixin, ListView):

    model = Project
    paginate_by = 10


class ProjectCreateView(LoginRequiredMixin, CreateView):

    model = Project


class ProjectUpdateView(LoginRequiredMixin, ProjectViewMixin, UpdateView):

    model = Project
    template_name_suffix = '_update_form'

    def get_object(self):
        return self.project


class ProjectDetailView(ProjectViewMixin, DetailView):

    model = Project

    def get_object(self):
        return self.project


class IssueListView(ProjectListView, ListView):

    model = Issue
    paginate_by = 10


class IssueCreateView(LoginRequiredMixin, ProjectViewMixin, PreviewFormMixin, CreateView):

    model = Issue
    form_class = IssueModelForm

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)
    
    def preview(self, form):
        self.preview_data = form.instance.description
        return super().preview(form)


class IssueUpdateView(LoginRequiredMixin, IssueViewMixin, PreviewFormMixin, UpdateView):

    model = Issue
    form_class = IssueModelForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        self.object = self.get_object()
        print(self.object.__dict__)
        form.instance.id = self.issue.id
        form.instance.project = self.issue.project
        form.instance.reporter = self.issue.reporter
        print(form.instance.__dict__)
        if form.changed_data:
            if self.issue.description != form.cleaned_data['description']:
                self.issue.changed(
                    self.request.user,
                    'description'
                )
            if self.issue.title != form.cleaned_data['title']:
                self.issue.changed(
                    self.request.user,
                    'title'
                )
        return super().form_valid(form)
    
    def preview(self, form):
        self.preview_data = form.instance.description
        return super().preview(form)

    def get_object(self):
        return self.issue


class IssueMetaUpdateView(LoginRequiredMixin, IssueViewMixin, UpdateView):

    model = Issue
    form_class = IssueMetaModelForm
    template_name_suffix = '_update_form'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        assignee = form.instance.assignee
        tags = form.instance.tags
        if form.is_valid():
            if form.changed_data:
                if assignee != None \
                        and form.cleaned_data['assignee'] == None:
                    self.object.unassign(
                        request.user
                    )
                if assignee == None \
                        and form.cleaned_data['assignee'] != None:
                    self.object.assign(
                        request.user,
                        form.cleaned_data['assignee']
                    )
            self.form_valid(form)
        else:
            self.form_invalid(form)
        return super().post(request, *args, **kwargs)

    def get_object(self):
        return self.issue


class IssueDetailDisplayView(IssueViewMixin, DetailView):

    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IssueCommentForm()
        context['tags'] = context['object'].tags.all()
        return context

    def get_object(self):
        return self.issue


class IssueDetailCommentView(SingleObjectMixin, IssueViewMixin, FormView):

    template_name = 'issuetracker/issue_detail.html'
    form_class = IssueCommentForm
    model = Issue

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            IssueComment.objects.create(
                issue=self.object,
                user=request.user,
                action='commented',
                icon='comment',
                text=form.cleaned_data["comment"]
            ).save()
        else:
            self.form_invalid(form)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('issuetracker:issue', kwargs={'pk': self.object.pk})

    def get_object(self):
        return self.issue


class IssueDetailView(View):

    def get(self, request, *args, **kwargs):
        view = IssueDetailDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = IssueDetailCommentView.as_view()
        return view(request, *args, **kwargs)


class IssueActionUpdateView(LoginRequiredMixin, IssueViewMixin, UpdateView):
    model = IssueAction
    fields = ['text']
    template_name_suffix = '_update_form'


class TagListView(ProjectViewMixin, ListView):

    model = Tag


class TagCreateView(LoginRequiredMixin, ProjectViewMixin, CreateView):

    model = Tag
    fields = ['name', 'color']

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, ProjectViewMixin, UpdateView):

    model = Tag
    fields = ['name', 'color']


class TagDetailView(ProjectViewMixin, DetailView):

    model = Tag


class SearchResultView(ListView):

    model = Issue
    
    def get_template_names(self):
        return 'issuetracker/search_result.html'

    def get_queryset(self):
        needle = self.kwargs['needle']
        ias = IssueComment.objects.filter(text__icontains=needle)
        pks = ias.values_list('issue', flat=True)
        return Issue.objects.filter(
            (Q(title__icontains=needle) | Q(description__icontains=needle)) \
            | Q(id__in=pks))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['needle'] = self.kwargs['needle']
        return context



class SearchView(FormView):

    form_class = SearchForm
    
    def get_success_url(self):
        return reverse_lazy('issuetracker:search_result', kwargs={'needle': self.needle})

    def form_valid(self, form):
        self.needle = form.cleaned_data['needle']
        return super().form_valid(form)
