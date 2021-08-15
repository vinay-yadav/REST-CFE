from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        content = data.get('content', None)
        image = data.get('image', None)

        if content == "" and image is None:
            raise forms.ValidationError('Either content or image is required')

        return data
