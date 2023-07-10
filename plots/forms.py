from django import forms
from multiupload.fields import MultiFileField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from django import forms
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['.txt', '.csv']  # Add the allowed file extensions here

def validate_file_extension(value):
    for file in value:
        file_extension = file.name.lower().split('.')[-1]
        print(file.name.lower().split('.')[-1])
        if file_extension not in ALLOWED_EXTENSIONS:
            raise ValidationError("Only {} files are allowed.".format(', '.join(ALLOWED_EXTENSIONS)))

class AbsForm(forms.Form):
    abs_files = MultiFileField(min_num=1, max_num=10, 
                               label="Abs Files",
                               )
        
    abs_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={'placeholder': 'Label 1, Label 2 ...'}),
                        label="Abs Labels",
                        required=False
                        ) 

    pl_files = MultiFileField(min_num=1, max_num=10,
                            label="PL Files",
                            required=False
                            )
    
    pl_labels = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Label 1, Label 2 ...'}),
                        label="PL Labels",
                        required=False
                        )

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Abs & PL'}),
                        label='Figure Title',
                        required=False,
                        )

class XrdForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['card_files'] = MultiFileField(
            min_num=1,
            max_num=10,
            label="Card Files",
            required=False
        )
        
        self.fields['card_file_labels'] = forms.CharField(
            widget=forms.TextInput(attrs={
                'class': 'cardfile_labels-input',
                'placeholder': 'Label 1, Label 2 ...'
                }),
            label="Card Labels",
            required=False
        )
        
        self.fields['xrd_files'] = MultiFileField(
            min_num = 1,
            max_num=10,
            label='Xrd Files',
        )

        self.fields['xrd_labels'] = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'placeholder': 'Label 1, Label 2 ...'
                                }),
                        label="Xrd Labels",
                        required=False
                        )
        
        self.fields['title'] = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'title-input',
                                'placeholder': 'Powder XRD'
                                   }),
                        label='Figure Title',
                        required=False,
                        help_text=''
                        )

        self.order_fields(field_order=['cardFiles', 'cardfile_labels'])
