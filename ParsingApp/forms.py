from django import forms
from .models import RawData

class RawDataForm(forms.Form):
    class Meta:
        model = RawData
        fields = '__all__'
