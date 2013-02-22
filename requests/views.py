from django.shortcuts import render
import forms


def new_request(http_request):
    form = forms.RequestForm()

    if http_request.method == "POST":
        form = forms.RequestForm(http_request.POST)
        if form.is_valid():
            form.save()
            form = forms.RequestForm()

    return render(http_request, "make_request.html", {'form': form})
