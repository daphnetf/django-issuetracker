from django import forms

class IssueActionCommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea
    )
