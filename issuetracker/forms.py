from django import forms

class IssueActionCommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea
    )

class SearchForm(forms.Form):
    needle = forms.CharField(
    )
