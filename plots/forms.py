from django import forms
from multiupload.fields import MultiFileField

class FileUploadForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=10,
                        label="Text Files")
    
    legend_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'legend-input',
                                'placeholder': 'Label 1, Label 2, Label 3 ...'
                                }),
                        label="Legend Labels",
                        required=False
                        ) 

    title = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'title-input',
                                'placeholder': 'Absorbance & Photoluminescence'
                                   }),
                        label='Figure Title',
                        required=False,
                        help_text=''
                        )

class XrdFileUploadForm(forms.Form):
    
    cardFiles = MultiFileField(min_num=1, max_num=10,
                        label="Card Files")
    
    files = MultiFileField(min_num=1, max_num=10,
                        label="Text Files")
    
    cardfile_labels = forms.CharField(
                    widget=forms.TextInput(attrs={'class': 'cardfile_labels-input'}),
                    label="Card File Labels"
                    ) 

    cardfile_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'cardfile_labels-input',
                                'placeholder': 'Label 1, Label 2, Label 3 ...'
                                }),
                        label="Card File Labels",
                        required=False
                        ) 

    legend_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'legend-input',
                                'placeholder': 'Label 1, Label 2, Label 3 ...'
                                }),
                        label="Legend Labels",
                        required=False
                        ) 

    title = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'title-input',
                                'placeholder': 'Powder XRD'
                                   }),
                        label='Figure Title',
                        required=False,
                        help_text=''
                        )

