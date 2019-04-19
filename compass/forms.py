from django import forms
from .models import UserDetails, Question_choice, Answer, Question

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


# we need
class AnswerChoiceForm(forms.ModelForm):
    answer = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.RadioSelect())
    comment = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        model = Question_choice
        fields = ('answer', 'comment')


    def __init__(self, question_id, *args, **kwargs):
        super(AnswerChoiceForm, self).__init__(*args, **kwargs)
        answers = Answer.objects.filter(question = question_id)
        self.fields["answer"].queryset = answers
        self.fields['answer'].widget.attrs = {
            'class': 'card-input-element'}
