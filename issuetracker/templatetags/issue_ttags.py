from django import template

register = template.Library()

@register.assignment_tag
def can_edit(issue, user):
    return issue.can_edit(user)

