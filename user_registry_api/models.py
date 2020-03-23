from re import search as re_search, compile as re_compile
from django.db import models
from django import forms
from django.utils.translation import ugettext as _

# Create your models here.
class UserRegistry(models.Model):
    class Meta:
        ordering = ['surname']

    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    email = models.CharField(unique=True, max_length=60)
    position = models.TextField()

    def __str__(self):
        return '%s %s' % (self.name, self.surname)

class Regex:
    number = re_compile('\d')
    emailAddress = re_compile('\w[\w\.-]*@\w[\w\.-]+\.\w+')

class UserRegistryForm(forms.ModelForm):
    class Meta:
        model = UserRegistry
        fields = [
            'name',
            'surname',
            'email',
            'position'
        ]

    class ValidationErrorCode:
        numbers_not_allowed = 'numbers_not_allowed'
        invalid_email_address = 'invalid email address'

    class ValidationErrrorMessage:
        this_field_cannot_contain_numbers = 'This field cannot contain numbers'
        this_field_must_contain_a_valid_email_address = 'This field must contain a valid email address'

    @staticmethod
    def non_numeric_validation(input):
        contains_number = bool(Regex.number.search(input))

        if contains_number:
            raise forms.ValidationError(
                _(UserRegistryForm.ValidationErrrorMessage.this_field_cannot_contain_numbers),
                code=UserRegistryForm.ValidationErrorCode.numbers_not_allowed
            )

        return input

    @staticmethod
    def email_validation(input):
        valid_email = bool(Regex.emailAddress.search(input))

        if not valid_email:
            raise forms.ValidationError(
                _(UserRegistryForm.ValidationErrrorMessage.this_field_must_contain_a_valid_email_address),
                code=UserRegistryForm.ValidationErrorCode.invalid_email_address
            )

        return input

    def clean_name(self):
        return UserRegistryForm.non_numeric_validation(self.cleaned_data['name'])

    def clean_surname(self):
        return UserRegistryForm.non_numeric_validation(self.cleaned_data['surname'])

    def clean_email(self):
        return UserRegistryForm.email_validation(self.cleaned_data['email'])

    def getResponseErrorData(self):
        errorData = {}
        errorFieldPrefix = self.Meta.model.__name__
        errorFieldKey = None

        for field in self.errors.keys():
            errorFieldKey = '%s.%s' % (errorFieldPrefix, field)
            if errorFieldKey not in errorData:
                errorData[errorFieldKey] = []

            for error in self.errors[field]:
                errorData[errorFieldKey].append({
                    'error': error
                })

        return errorData

class UserRegistryUpdateForm(forms.ModelForm):
    name = forms.CharField(required=False)
    surname = forms.CharField(required=False)
    email = forms.CharField(required=False)
    position = forms.CharField(required=False)

    class Meta:
        model = UserRegistry
        fields = [
            'name',
            'surname',
            'email',
            'position'
        ]