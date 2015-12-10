from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from issuetracker.models import Project, Issue

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

