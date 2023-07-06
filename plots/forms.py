from django import forms
from multiupload.fields import MultiFileField

class AbsForm(forms.Form):
    abs_files = MultiFileField(min_num=1, max_num=10,
                        label="Abs Files")
    
    abs_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={'placeholder': 'Label 1, Label 2 ...'}),
                        label="Abs Labels",
                        required=False
                        ) 

    pl_files = MultiFileField(min_num=1, 
                        max_num=10,
                        label="PL Files",
                        required=False
                        )
    
    pl_labels = forms.CharField(
                        widget=forms.TextInput(
                            attrs={'placeholder': 'Label 1, Label 2 ...'}),
                        label="PL Labels",
                        required=False
                        )

    title = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'title-input',
                                'placeholder': 'Abs & PL'
                                   }),
                        label='Figure Title',
                        required=False,
                        help_text=''
                        )

class XrdForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['cardFiles'] = MultiFileField(
            min_num=1,
            max_num=10,
            label="Card Files"
        )
        
        self.fields['cardfile_labels'] = forms.CharField(
            widget=forms.TextInput(attrs={
                'class': 'cardfile_labels-input',
                'placeholder': 'Label 1, Label 2 ...'
                }),
            label="Card Labels",
            required=False
        )
        
        self.fields['files'] = MultiFileField(
            label='Xrd Files',
        )

        self.fields['legend_labels'] = forms.CharField(
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
