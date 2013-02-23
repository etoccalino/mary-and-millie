from django.forms.models import inlineformset_factory
from django import forms
import models


MAX_ITEMS = 3
ItemRequestFormSet = inlineformset_factory(models.Request, models.ItemRequest,
                                           can_delete=False, extra=MAX_ITEMS)


class RequestForm(forms.ModelForm):

    class Meta:
        model = models.Request
        fields = ('location',)


class AssociateRequestForm(forms.Form):
    bin = forms.ModelChoiceField(
        queryset=models.Bin.objects.filter(requested=False),
        empty_label="(select a bin)")
