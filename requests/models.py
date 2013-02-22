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

    def __unicode__(self):
        return unicode(self.number)


class Request(models.Model):
    location = models.ForeignKey(Location)

    bin = models.ForeignKey(Bin, null=True)

    request_time = models.DateTimeField(auto_now_add=True)
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
