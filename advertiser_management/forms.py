from django import forms

from advertiser_management.models import Ad


class CreateNewAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('advertiser', 'title', 'img_url')
        widgets = {
            'advertiser': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'img_url': forms.FileInput(attrs={'class': 'form-control'}),
        }
