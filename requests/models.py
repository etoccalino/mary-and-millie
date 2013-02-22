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
    items = models.ManyToManyField(Item, through='ItemRequest')

    bin = models.ForeignKey(Bin, null=True)

    request_time = models.DateTimeField(auto_now_add=True)
    done_time = models.DateTimeField()


class ItemRequest(models.Model):
    request = models.ForeignKey(Request)
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s %s" % (self.quantity, self.item)
