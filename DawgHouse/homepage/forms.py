from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import DawgHouseUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = DawgHouseUser
        fields = ['username', 'first_name', 'last_name', 'password']
        error_messages = {
            'username': {
                'unique': ("A user with that dawgtag already exists."),
            },
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password, self.instance)
        except ValidationError as error:
            raise forms.ValidationError(list(error.messages))
        return password

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

