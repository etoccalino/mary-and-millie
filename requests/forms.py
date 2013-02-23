from django.forms.models import inlineformset_factory
from django import forms
import models


EXTRA_ITEMS = 3
MAX_ITEMS = 5
ItemRequestFormSet = inlineformset_factory(models.Request, models.ItemRequest,
                                           can_delete=False, extra=EXTRA_ITEMS,
                                           max_num=MAX_ITEMS)


class RequestForm(forms.ModelForm):

    class Meta:
        model = models.Request
        fields = ('location',)


class AssociateRequestForm(forms.Form):
    bin = forms.ModelChoiceField(
        queryset=models.Bin.objects.filter(requested=False),
        empty_label="(select a bin)")
