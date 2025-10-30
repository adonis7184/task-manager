from django import forms

class TechForm(forms.Form):
    template_name = "devs/teches/form_snippet.html"

    name = forms.CharField(label='Tech Name', max_length=15, min_length=5)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={"cols": 40, "rows": 10}),
        required=False,
    )