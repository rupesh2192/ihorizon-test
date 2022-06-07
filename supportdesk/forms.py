from django.forms import ModelForm, TextInput, Textarea

from supportdesk.models import Request


class CreateRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['summary', 'description', "is_high_priority"]
        widgets = {
            'summary': TextInput(attrs={"class": "form-control", "placeholder": "Unable to login to application"}),
            'description': Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "is_high_priority": "Flag as high priority"
        }
