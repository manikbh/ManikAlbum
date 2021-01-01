# -*- coding: utf-8 -*-
from django import forms

class PhotoUploadForm(forms.Form):
    file = forms.ImageField(
        label='Select a photo',
        help_text='Choose file to upload',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    albumpk = forms.IntegerField(widget=forms.HiddenInput(), initial=-1)
