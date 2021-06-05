from django import forms


class UploadForm(forms.Form):
    img = forms.ImageField(label="Choose your image")
