from django import forms
from .models import UserDetails, Question_choice, Answer, Business_Priority

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('first_name', 'last_name', 'email', 'company', 'role')

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
        self.fields['email'].error_messages['unique'] = 'This email has already registered'
        self.fields['company'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Company',
            'placeholder': 'Company'}
        self.fields['role'].widget.attrs = {
            'class': 'form-control my-input',
            'name': 'Role',
            'placeholder': 'Role'}


class AnswerChoiceForm(forms.ModelForm):
    answer = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.RadioSelect())
    comment = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        model = Question_choice
        fields = ('answer', 'comment')


    def __init__(self, question_id, *args, **kwargs):
        super(AnswerChoiceForm, self).__init__(*args, **kwargs)
        answers = Answer.objects.filter(question = question_id).order_by('score')
        self.fields["answer"].queryset = answers


class BusinessPriorityForm(forms.ModelForm):
    data_quality = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'value': '1', 'min': '1', 'max': '3'}), required=True)
    cat_modeling = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'value': '1', 'min': '1', 'max': '3'}), required=True)
    non_modelled = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'value': '1', 'min': '1', 'max': '3'}), required=True)
    profiling_submissions = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'value': '1', 'min': '1', 'max': '3'}), required=True)

    class Meta:
        model = Business_Priority
        fields = ('data_quality', 'cat_modeling', 'non_modelled', 'profiling_submissions')

    def __init__(self, *args, **kwargs):
        super(BusinessPriorityForm, self).__init__(*args, **kwargs)
        self.fields['data_quality'].widget.attrs = {
            'class': 'slider',
            'min': 1,
            'max': 3,
            'value': 2}
        self.fields['cat_modeling'].widget.attrs = {
            'class': 'slider',
            'min': 1,
            'max': 3,
            'value': 2}
        self.fields['non_modelled'].widget.attrs = {
            'class': 'slider',
            'min': 1,
            'max': 3,
            'value': 2}
        self.fields['profiling_submissions'].widget.attrs = {
            'class': 'slider',
            'min': 1,
            'max': 3,
            'value': 2}

