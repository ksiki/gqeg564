from django import forms
from django.core.validators import FileExtensionValidator


class UploadJSONForm(forms.Form):
    file = forms.FileField(
        label="Choose JSON file:",
        validators=[FileExtensionValidator(allowed_extensions=["json"])],
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".json"}),
    )
