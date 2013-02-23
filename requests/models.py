from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

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

    def __unicode__(self):
        result = u""
        for item in self.items.all():
            if result:
                result = u"%s and" % result
            result = u"%s %s" % (result, item)
        if not result:
            return u"empty request for %s" % self.location
        return u"%s for %s" % (result, self.location)


class ItemRequest(models.Model):
    request = models.ForeignKey(Request, related_name="items")
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s %s" % (self.quantity, self.item)
