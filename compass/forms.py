from django import forms
from .models import UserDetails

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('first_name', 'last_name', 'email', 'company', 'sector', 'role')

    # we can take a look at Django widget tweaks but wan't to keep the dependencies to a min
    def __init__(self, *args, **kwargs):
        super(UserDetailForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'First Name',
            'placeholder': 'First Name'}
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Last Name',
            'placeholder': 'Last Name'}
        self.fields['email'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Email',
            'type': 'email',
            'placeholder': 'Email'}
        self.fields['company'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Company',
            'placeholder': 'Company'}
        self.fields['sector'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Sector',
            'placeholder': 'Sector'}
        self.fields['role'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Role',
            'placeholder': 'Role'}

