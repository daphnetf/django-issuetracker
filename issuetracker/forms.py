from django import forms

from issuetracker.models import Issue


class IssueActionCommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea
    )

class SearchForm(forms.Form):
    needle = forms.CharField(
    )

class IssueModelForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['title', 'description']

class IssueMetaModelForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['assignee', 'tags']
        widgets = {'tags': forms.CheckboxSelectMultiple}
