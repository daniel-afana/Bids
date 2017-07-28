from django.db import models
from django.contrib.postgres.fields import ArrayField


class Channel(models.Model):

    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    BID_TYPES_CHOICES = (
        ("CPC", "CPC"),
        ("CPM", "CPM"),
        ("CPA", "CPA"),
        ("CPV", "CPV"),
        ("CPI", "CPI"),
    )
    bid_types = ArrayField(
        models.CharField(choices=BID_TYPES_CHOICES, max_length=3, default="CPM"),
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    
    name = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    bid = models.FloatField(blank=True)
    bid_type = models.CharField(max_length=3)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        bid_type = bid_type.upper()
        if self.bid_type not in self.channel.bidtypes:
            raise ValidationError("Please, specify one of the bid types that belongs to the selected channel: {}",
            self.channel.bid_types)
        super(Campaign, self).save(*args, **kwargs)