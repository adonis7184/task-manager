from django import forms
from devs.models import Tech

class TeamForm(forms.Form):

    name = forms.CharField(label='Team Name', max_length=15, min_length=5)
    teches = forms.ModelMultipleChoiceField(
        queryset=Tech.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )