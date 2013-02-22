from django import forms
import models


class RequestForm(forms.ModelForm):

    class Meta:
        model = models.Request
        exclude = ('request_time', 'done_time', 'bin',)


class DoneRequestForm(forms.ModelForm):

    class Meta:
        model = models.Request
