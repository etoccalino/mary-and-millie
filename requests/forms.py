import django.forms
from crispy_forms.helper import FormHelper
from django.forms.formsets import formset_factory
import models


class ItemRequestForm(django.forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(ItemRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.ItemRequest
        fields = ('item', 'quantity')


MAX_ITEMS = 3
ItemRequestFormSet = formset_factory(ItemRequestForm, extra=MAX_ITEMS)


class RequestForm(django.forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(RequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Request
        fields = ('location',)


class AssociateRequestForm(django.forms.Form):
    bin = django.forms.ModelChoiceField(
        queryset=models.Bin.objects.filter(requested=False),
        empty_label="(select a bin)")
