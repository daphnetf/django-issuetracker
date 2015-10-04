from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from issuetracker.models import Issue, Tag, IssueAction


class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)


class IssueAdmin(admin.ModelAdmin):
    pass
admin.site.register(Issue, IssueAdmin)


class IssueActionAdmin(MarkdownModelAdmin):
    pass
admin.site.register(IssueAction, IssueActionAdmin)
