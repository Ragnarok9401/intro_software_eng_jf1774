from django import forms
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.core.exceptions import ValidationError
from .models import DawgHouseUser

class CustomUserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields did not match.",
    }
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    retype_password = forms.CharField(label='Retype Password', widget=forms.PasswordInput)

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

        if password and retype_password and password != retype_password:
            self.add_error('retype_password', self.error_messages['password_mismatch'])

        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                for validator in get_default_password_validators():
                    try:
                        validator.validate(password, self.instance)
                    except ValidationError as e:
                        self.add_error('password', e)

        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'DawgTag', 'class': 'input-field', 'required': True}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-field', 'required': True}))

class EditUserForm(forms.ModelForm):
    bio = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your bio: "}))

    class Meta:
        model = DawgHouseUser
        fields = ['bio']
        