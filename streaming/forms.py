from django import forms

class StorageForm(forms.Form):
  link = forms.CharField(label='Connect to your storage', widget=forms.TextInput(attrs={'class': "form-control"}))

class SongUploadForm(forms.Form):
  name = forms.CharField(label='Song name', widget=forms.TextInput(attrs={'class': "form-control"}))
  thumbnail = forms.FileField(label='Thumbnail', widget=forms.FileInput(attrs={'class': "form-control"}))
  song_file = forms.FileField(label='Mp3 file', widget=forms.FileInput(attrs={'class': "form-control"}))

class PlaylistForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': "form-control"}))