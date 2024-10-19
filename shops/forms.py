from django import forms
from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'latitude', 'longitude']

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude < -90 or latitude > 90:
            raise forms.ValidationError('Invalid latitude. Latitude must be between -90 and 90.')
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude < -180 or longitude > 180:
            raise forms.ValidationError('Invalid longitude. Longitude must be between -180 and 180.')
        return longitude
