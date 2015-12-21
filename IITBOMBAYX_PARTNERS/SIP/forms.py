from django import forms
from models import uploadedfiles

class EmailForm(forms.Form):
    sender = forms.EmailField()
    receiver = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)    
    cc_myself = forms.BooleanField(required=False)

class UploadForms(forms.ModelForm):
    
    class  Meta:
        model = uploadedfiles
        fields = ('filename',)
        


