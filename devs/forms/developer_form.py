from django import forms
from devs.models import Developer
from django.conf import settings
# widgets.py
from django import forms
from django.utils.safestring import mark_safe

class IntlTelInputWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.19/build/css/intlTelInput.css',)
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/intlTelInput.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js',
        )

    def __init__(self, attrs=None, preferred_countries=None, initial_country='auto'):
        super().__init__(attrs)
        self.preferred_countries = preferred_countries or ['us', 'gb']
        self.initial_country = initial_country
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        input_id = attrs.get('id') or f'id_{name}'
        attrs['id'] = input_id
        input_html = super().render(name, value, attrs, renderer)
        js = f"""
        <script>
          const input = document.querySelector("#{input_id}");
          if(input) {{
            window.intlTelInput(input, {{
              initialCountry: "{self.initial_country}",
              preferredCountries: {self.preferred_countries},
              utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js"
            }});
          }}
        </script>
        """
        return mark_safe(f"{input_html}{js}")

class DeveloperForm(forms.ModelForm):
    # template_name = "tasks/developers/form_snippet.html"

    class Meta:
        model = Developer
        fields = '__all__' 
        exclude = ['date_registered',] 
        widgets = {
            'phone_number': IntlTelInputWidget(
                initial_country = settings.PHONENUMBER_DEFAULT_REGION.lower(),
                attrs={'id': 'phone_number_input'}
            )
        }