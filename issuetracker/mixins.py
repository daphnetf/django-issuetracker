from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from issuetracker.models import Project, Issue, Tag

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ProjectViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        pk = None
        if 'pk' in kwargs:
            pk = int(kwargs.pop('pk'))
        if 'project' in kwargs:
            pk = int(kwargs.pop('project'))
        self.project = get_object_or_404(
            Project,
            pk=pk
        )
        return super().dispatch(request, *args, **kwargs)


class IssueViewMixin(ProjectViewMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = None
        if 'pk' in kwargs:
            pk = int(kwargs.pop('pk'))
        if 'issue' in kwargs:
            pk = int(kwargs.pop('issue'))
        self.issue = get_object_or_404(
            Issue,
            pk=pk
        )
        return super().dispatch(request, *args, **kwargs)


class TagViewMixin(ProjectViewMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = None
        if 'pk' in kwargs:
            pk = int(kwargs.pop('pk'))
        if 'tag' in kwargs:
            pk = int(kwargs.pop('tag'))
        self.tag = get_object_or_404(
            Tag,
            pk=pk
        )
        return super().dispatch(request, *args, **kwargs)


class PreviewFormMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.preview_mode = False
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not hasattr(self, 'object'):
            self.object = None
        self.preview_data = ''
        form = self.get_form()
        valid = form.is_valid()
        if 'preview' in request.POST:
            return self.preview(form)
        if 'edit' in request.POST:
            return self.form_invalid(form)
        if valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def preview(self, form):
        self.preview_mode = True
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_preview_mode'] = True
        context['preview_mode'] = self.preview_mode
        if context['preview_mode']:
            context['preview'] = self.preview_data
        return context