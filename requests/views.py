from django.shortcuts import render, get_object_or_404
import models
import forms


def requests(http_request):
    requests = models.Request.objects.all()
    return render(http_request, "requests.html", {'requests': requests})


def request(http_request, request_pk):
    request = get_object_or_404(models.Request, pk=request_pk)
    return render(http_request, "request.html", {'request': request})


def new_request(http_request):
    form = forms.RequestForm()
    items_formset = forms.ItemRequestFormSet()

    if http_request.method == "POST":
        form = forms.RequestForm(http_request.POST)
        items_formset = forms.ItemRequestFormSet(http_request.POST)
        if form.is_valid() and items_formset.is_valid():
            request = form.save()
            for item_data in items_formset.cleaned_data:
                if item_data:
                    item_request = models.ItemRequest()
                    item_request.request = request
                    item_request.item = item_data['item']
                    item_request.quantity = item_data['quantity']
                    item_request.save()

            form = forms.RequestForm()
            items_formset = forms.ItemRequestFormSet()

    return render(http_request, "make_request.html",
                  {'form': form, 'items_formset': items_formset})
