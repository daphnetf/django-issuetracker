from django import template

register = template.Library()

@register.assignment_tag
def can_edit(obj, user):
    if hasattr(obj, 'can_edit'):
        return obj.can_edit(user)
    return False
