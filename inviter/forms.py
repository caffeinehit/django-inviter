from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        # Hide the UUID string
        self.initial['username'] = ''
        self.fields['password'].help_text = ''
        

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
    
    def save(self, *args, **kwargs):
        user = super(RegistrationForm, self).save(*args,**kwargs)
        user.set_password(self.cleaned_data.get('password'))
        user.is_active = True
        user.save()
        return user
    
    