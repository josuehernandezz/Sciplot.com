from django import forms
from multiupload.fields import MultiFileField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from django import forms
from django.core.exceptions import ValidationError

class UniversalForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=10, 
                               label="Files",
                               )
        
    labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={'placeholder': 'Label 1, Label 2 ...'}),
                        label="Labels",
                        required=False
                        ) 

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Figure Title'}),
                        label='Figure Title',
                        required=False,
                        )

    theme = forms.ChoiceField(required=False, choices=( 
                        ("", "Standard"), 
                        ("dark", "Dark")))

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
    
    norm_num_abs = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': 'Default value is y max'}),
        label='Normalize to x',
        required=False)

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Abs & PL'}),
                        label='Figure Title',
                        required=False,
                        )

    theme = forms.ChoiceField(required=False, choices=( 
                        ("", "Standard"), 
                        ("dark", "Dark")))

class FTIRForm(forms.Form):
    ftir_files = MultiFileField(min_num=1, max_num=10, 
                               label="FTIR Files",
                               )
        
    ftir_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={'placeholder': 'Label 1, Label 2 ...'}),
                        label="FTIR Labels",
                        required=False
                        ) 

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'FTIR'}),
                        label='Figure Title',
                        required=False,
                        )

    theme = forms.ChoiceField(required=False, choices=( 
                        ("", "Standard"), 
                        ("dark", "Dark")))

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
        
        self.fields['theme'] = forms.ChoiceField(required=False, choices=( 
                    ("", "Standard"), 
                    ("dark", "Dark")))

class PLQYForm(forms.Form):
    cor_file = MultiFileField(min_num=0, max_num=10, 
                               label="Correction File",
                               )
        
    cor_label = forms.CharField(
                        widget=forms.TextInput(
                        attrs={'placeholder': 'Correction'}),
                        label="Correction Label",
                        required=False
                        )

    blk_file = MultiFileField(min_num=1, max_num=10, 
                               label="Blank File",
                               )
        
    blk_label = forms.CharField(
                        widget=forms.TextInput(
                        attrs={'placeholder': 'Blank'}),
                        label="Blank Label",
                        required=False
                        ) 

    sct_file = MultiFileField(min_num=0, max_num=10,
                            label="Scatter File",
                            required=False
                            )
    
    sct_label = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Scatter'}),
                        label="Scatter Label",
                        required=False
                        )

    emi_file = MultiFileField(min_num=0, max_num=10,
                            label="Emission File",
                            required=False
                            )
    
    emi_label = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Emission'}),
                        label="Emission Label",
                        required=False
                        )

    checkbox = forms.BooleanField(
        label="Check to neglect reabsorption correction",
        required=False,
    )

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'PLQY'}),
                        label='Figure Title',
                        required=False,
                        )

    theme = forms.ChoiceField(required=False, choices=( 
                        ("", "Standard"), 
                        ("dark", "Dark")))
