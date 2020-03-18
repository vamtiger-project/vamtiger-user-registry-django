from django.db import models
from django import forms

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

class UserRegistryForm(forms.ModelForm):
    class Meta:
        model = UserRegistry
        fields = [
            'name',
            'surname',
            'email',
            'position'
        ]

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