from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import DawgHouseUser

class CustomUserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields did not match."
    }
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    retype_password = forms.CharField(label='Retype Password', widget=forms.PasswordInput, error_messages={'required': 'The two password fields did not match.'})

    class Meta:
        model = DawgHouseUser
        fields = ['username', 'first_name', 'last_name', 'password']
        error_messages = {
            'username': {
                'unique': ("A user with that dawgtag already exists."),
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        retype_password = cleaned_data.get('retype_password')

        if password and retype_password:
            if password != retype_password:
                self.add_error('retype_password', self.error_messages['password_mismatch'])

        try:
            validate_password(password, self.instance)
        except ValidationError as error:
            raise forms.ValidationError(list(error.messages))

        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

