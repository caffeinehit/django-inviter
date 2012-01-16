from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegistrationForm(forms.ModelForm):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        # Hide the UUID string
        self.initial['username'] = ''

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, *args, **kwargs):
        user = super(RegistrationForm, self).save(*args,**kwargs)
        user.set_password(self.cleaned_data.get('new_password1'))
        user.is_active = True
        if kwargs.get('commit', True):
            user.save()
        return user
    
    