import django.forms
from crispy_forms.helper import FormHelper
from django.forms.models import inlineformset_factory
import models


class ItemRequestForm(django.forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(ItemRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.ItemRequest
        fields = ('item', 'quantity')


MAX_ITEMS = 5
EXTRA_ITEMS = 3
ItemRequestFormSet = inlineformset_factory(
                         models.Request, models.ItemRequest,
                         form=ItemRequestForm, can_delete=False,
                         extra=EXTRA_ITEMS, max_num=MAX_ITEMS)


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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(AssociateRequestForm, self).__init__(*args, **kwargs)
