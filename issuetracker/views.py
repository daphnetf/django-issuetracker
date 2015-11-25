from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, TemplateView, FormView, View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from issuetracker.forms import IssueActionCommentForm, SearchForm, \
    IssueModelForm, IssueMetaModelForm
from issuetracker.mixins import LoginRequiredMixin
from issuetracker.models import Issue, IssueAction, Tag



class HomeView(TemplateView):

    template_name = 'issuetracker/home.html'


class IssueListView(ListView):

    model = Issue
    paginate_by = 10


class IssueCreateView(LoginRequiredMixin, CreateView):

    model = Issue
    form_class = IssueModelForm

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class IssueUpdateView(UpdateView):

    model = Issue
    form_class = IssueModelForm
    template_name_suffix = '_update_form'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        title = form.instance.title
        description = form.instance.description
        if form.is_valid():
            if form.changed_data:
                if description != form.cleaned_data['description']:
                    self.object.changed(
                        request.user,
                        'description'
                    )
                if title != form.cleaned_data['title']:
                    self.object.changed(
                        request.user,
                        'title'
                    )
            self.form_valid(form)
        else:
            self.form_invalid(form)
        return super().post(request, *args, **kwargs)


class IssueMetaUpdateView(UpdateView):

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


class IssueDetailDisplayView(DetailView):

    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IssueActionCommentForm()
        context['tags'] = context['object'].tags.all()
        context['actions'] = IssueAction.objects.filter(
            issue=context['object']
        )
        return context


class IssueDetailCommentView(SingleObjectMixin, FormView):

    template_name = 'issuetracker/issue_detail.html'
    form_class = IssueActionCommentForm
    model = Issue

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            IssueAction.objects.create(
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


class IssueDetailView(View):

    def get(self, request, *args, **kwargs):
        view = IssueDetailDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = IssueDetailCommentView.as_view()
        return view(request, *args, **kwargs)


class IssueActionUpdateView(UpdateView):
    model = IssueAction
    fields = ['text']
    template_name_suffix = '_update_form'


class TagListView(ListView):

    model = Tag


class TagCreateView(LoginRequiredMixin, CreateView):

    model = Tag
    fields = ['name', 'color']


class TagDetailView(DetailView):

    model = Tag


class SearchResultView(ListView):

    model = Issue
    
    def get_template_names(self):
        return 'issuetracker/search_result.html'

    def get_queryset(self):
        needle = self.kwargs['needle']
        ias = IssueAction.objects.filter(text__icontains=needle)
        pks = ias.values_list('issue', flat=True)
        return Issue.objects.filter(Q(title__icontains=needle) | Q(id__in=pks))

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
