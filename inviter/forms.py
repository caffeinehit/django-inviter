from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from inviter.models import OptOut


class RegistrationForm(forms.ModelForm):
    """ The standard form that is displayed to users when registering. It gives
    a user the option to change their email address. """
    email = forms.EmailField(label=_("Email address"))
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
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
        user = super(RegistrationForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data.get('new_password1'))
        user.is_active = True
        if kwargs.get('commit', True):
            user.save()
        return user
    

class OptOutForm(forms.ModelForm):
    """ Dummy form for opting out. """
    class Meta:
        model = User
        fields = ()
    
    def save(self):
        """ Delete the user object from the database and store the SHA1 hashed
        email address in the database to make sure this person does not receive
        any further invitation emails. """
        
        email = self.instance.email
        self.instance.delete()
        return OptOut.objects.create(email=email)
