from django.shortcuts import render, get_object_or_404
from random import randrange
from socketio import socketio_manage
import gevent
import namespace
import queue
import models
import forms

import logging
logger = logging.getLogger('app.views')


###############################################################################

CONSUMER_TIME_LOWER = 5  # seconds.
CONSUMER_TIME_UPPER = 10  # seconds.


def consumer(request, consumer_time=CONSUMER_TIME_LOWER):
    """Takes a request to have it "done"."""
    gevent.sleep(consumer_time)
    request.done()

###############################################################################


def socketio(http_request):
    return socketio_manage(http_request.environ,
                           {'/requests': namespace.Requests},
                           http_request)


def requests(http_request):
    requests = {
        'new': models.Request.objects.filter(
            status=models.Request.NEW_STATUS).order_by('-request_time'),
        'done': models.Request.objects.filter(
            status=models.Request.DONE_STATUS).order_by('-done_time'),
        'pending': models.Request.objects.filter(
            status=models.Request.PENDING_STATUS).order_by('-pending_time'),
        }
    return render(http_request, "requests.html", requests)


def request(http_request, request_pk):
    request = get_object_or_404(models.Request, pk=request_pk)
    form = forms.AssociateRequestForm(initial={'bin': request.bin})

    if http_request.method == "POST":
        form = forms.AssociateRequestForm(http_request.POST)
        if form.is_valid():
            bin = form.cleaned_data['bin']
            # Update the request and bin.
            request.pending(bin)
            bin.requested = True
            bin.save()

            # Launch the request consumer.
            consumer_time = randrange(CONSUMER_TIME_LOWER,
                                      CONSUMER_TIME_UPPER, 1)
            logger.debug("request consumer launched (it'll take %s seconds)."
                         % consumer_time)
            gevent.spawn(consumer, request, consumer_time=consumer_time)

            # Return to the requests list.
            return requests(http_request)

    return render(http_request, "request.html",
                  {'request': request, 'form': form})


def new_request(http_request):
    form = forms.RequestForm()
    items_formset = forms.ItemRequestFormSet()

    if http_request.method == "POST":
        form = forms.RequestForm(http_request.POST)
        items_formset = forms.ItemRequestFormSet(http_request.POST)
        if form.is_valid() and items_formset.is_valid():
            logger.debug("creating the new request.")
            request = form.save()
            for item_data in items_formset.cleaned_data:
                if item_data:
                    logger.debug("adding a new item.")
                    item_request = models.ItemRequest()
                    item_request.request = request
                    item_request.item = item_data['item']
                    item_request.quantity = item_data['quantity']
                    item_request.save()
            logger.debug("new request created.")

            logger.debug("Sending new request to the queue.")
            queue.put(request)

            form = forms.RequestForm()
            items_formset = forms.ItemRequestFormSet()

    return render(http_request, "new_request.html",
                  {'form': form, 'items_formset': items_formset})
