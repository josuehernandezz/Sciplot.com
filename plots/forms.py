from django import forms
from multiupload.fields import MultiFileField

class FileUploadForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=10)
    legend_labels = forms.CharField(widget=forms.TextInput(attrs={'class': 'legend-input'})) 
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title-input'}))
    # x_label = forms.CharField(widget=forms.TextInput(attrs={'class': 'xlabel-input'}))
    # y_label = forms.CharField(widget=forms.TextInput(attrs={'class': 'ylabel-input'}))
    # x_axis_min = forms.FloatField(label='X-Axis Min')
    # x_axis_max = forms.FloatField(label='X-Axis Max')
    # y_axis_min = forms.FloatField(label='Y-Axis Min')
    # y_axis_max = forms.FloatField(label='Y-Axis Max')

class XrdFileUploadForm(forms.Form):
    cardFiles = MultiFileField(min_num=1, max_num=10)
    files = MultiFileField(min_num=1, max_num=10)
    cardfile_labels = forms.CharField(widget=forms.TextInput(attrs={'class': 'cardfile_labels-input'})) 
    legend_labels = forms.CharField(widget=forms.TextInput(attrs={'class': 'legend-input'})) 
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title-input'}))
    # x_label = forms.CharField(widget=forms.TextInput(attrs={'class': 'xlabel-input'}))
    # y_label = forms.CharField(widget=forms.TextInput(attrs={'class': 'ylabel-input'}))
    # x_axis_min = forms.FloatField(label='X-Axis Min')
    # x_axis_max = forms.FloatField(label='X-Axis Max')
    # y_axis_min = forms.FloatField(label='Y-Axis Min')
    # y_axis_max = forms.FloatField(label='Y-Axis Max')
