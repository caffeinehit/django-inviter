from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        # Hide the UUID string
        self.fields['username'].initial = ''

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
    
    