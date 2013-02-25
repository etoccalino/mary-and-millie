from django.db import models
from django.utils.timezone import now
from django.core.serializers.json import DjangoJSONEncoder
import json


class Item(models.Model):
    name = models.CharField(max_length=100)

    def serialize(self, shape='json'):
        obj = self.name
        if shape == 'json':
            obj = json.dumps(obj, cls=DjangoJSONEncoder)
        return obj

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

    def serialize(self, shape='json'):
        obj = self.name
        if shape == 'json':
            obj = json.dumps(obj, cls=DjangoJSONEncoder)
        return obj

    def __unicode__(self):
        return self.name


class Bin(models.Model):
    number = models.PositiveIntegerField(primary_key=True)

    # Whether the bin is currently associated to a request.
    requested = models.BooleanField(default=False)

    def current_request(self):
        """Returns the Request instance associated to this bin.

        If the bin not associated to any request, returns None.
        """
        if not self.requested:
            return None
        try:
            request = self.request_set.get(status=Request.PENDING_STATUS)
        except Request.MultipleObjectsReturned:
            raise RuntimeError("More than one Request instance associated to "
                               "the same bin (bin %s)." % self.number)
        return request

    def serialize(self, shape='json'):
        obj = {
            'number': self.number,
            'requested': self.requested,
            }
        if shape == 'json':
            obj = json.dumps(obj, cls=DjangoJSONEncoder)
        return obj

    def __unicode__(self):
        return "bin %s" % self.number


class Request(models.Model):
    NEW_STATUS = 'new'
    PENDING_STATUS = 'pend'
    DONE_STATUS = 'done'
    ERROR_STATUS = 'err'
    STATUS = (
        (NEW_STATUS, 'New'),
        (PENDING_STATUS, 'Pending'),
        (DONE_STATUS, 'Done'),
        (ERROR_STATUS, 'Error'),
        )
    status = models.CharField(max_length=4, choices=STATUS, default=NEW_STATUS)

    location = models.ForeignKey(Location)
    bin = models.ForeignKey(Bin, null=True)

    # Date and time this request was made.
    request_time = models.DateTimeField(auto_now_add=True)
    # Date and time this request was associated with a bin and sent away.
    pending_time = models.DateTimeField(null=True)
    # Date and time this request was "done" (delived, finished).
    done_time = models.DateTimeField(null=True)

    def pending(self, bin=None):
        self.status = self.PENDING_STATUS
        if bin:
            self.bin = bin
            bin.requested = True
            bin.save()
        self.pending_time = now()
        self.save()

    def done(self):
        self.status = self.DONE_STATUS
        if self.bin:
            bin = self.bin
            bin.requested = False
            bin.save()
            self.bin = None
        self.done_time = now()
        self.save()

    def serialize(self, shape='json'):
        obj = {
            'meta': {
                'description': unicode(self),
                'url': self.get_absolute_url(),
                },
            'status': self.get_status_display(),
            'location': self.location.serialize(shape='dict'),
            'request_time': self.request_time,
            }
        items = []
        for item_request in self.items.all():
            items.append(item_request.serialize(shape='dict'))
        obj['items'] = items

        if self.bin:
            obj['bin'] = self.bin.serialize(shape='dict')
        if self.pending_time:
            obj['pending_time'] = self.pending_time
        if self.done_time:
            obj['done_time'] = self.done_time

        if shape == 'json':
            obj = json.dumps(obj, cls=DjangoJSONEncoder)
        return obj

    def __unicode__(self):
        result = u""
        for item in self.items.all():
            if result:
                result = u"%s and" % result
            result = u"%s %s" % (result, item)
        if not result:
            return u"empty request for %s" % self.location
        return u"%s for %s" % (result, self.location)

    @models.permalink
    def get_absolute_url(self):
        return ('request', (), {'request_pk': str(self.pk)})


class ItemRequest(models.Model):
    request = models.ForeignKey(Request, related_name="items")
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField()

    def serialize(self, shape='json'):
        obj = {
            'item': self.item.name,
            'quantity': self.quantity,
            }
        if shape == 'json':
            obj = json.dumps(obj, cls=DjangoJSONEncoder)
        return obj

    def __unicode__(self):
        return "%s %s" % (self.quantity, self.item)
