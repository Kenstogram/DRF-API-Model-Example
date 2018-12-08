#models
#import uuid
#import django_tables2 as tables
import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import utc
from phonenumber_field.modelfields import PhoneNumberField

BOOL_CHOICES = ((True, 'Waiting'), (False, 'Seated'))


class Profile(models.Model):
    name = models.CharField(max_length=30)
    contact = PhoneNumberField(blank=True)
    image = models.ImageField(upload_to = 'static/', default = 'static/None/no-img.jpg')
    location = models.CharField(max_length=30)
    city = models.CharField(max_length=30)


class Restaurant(models.Model):
    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contact = PhoneNumberField(blank=True)
    location = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    #    features = models.ManyToManyField() # dinner, launch, nightlife,
    #    timing = models.ManyToManyField() # sunday, monday, tuesday,
    delivery = models.BooleanField(default=False)


class Table(models.Model):
    name = models.CharField(max_length=30)
#    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    partysize = models.IntegerField()
    arrival_time = models.DateTimeField(auto_now_add=True, editable=False)
    contact = PhoneNumberField(blank=True)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)
    owner = models.ForeignKey('auth.User', default='1' , related_name='tables', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def get_time_diff(self):
        if self.arrival_time:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.arrival_time
            return timediff.total_seconds()

    wait = get_time_diff

    def save(self, *args, **kwargs):
        super(Table, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

        class Meta:
            verbose_name = 'Table'
            verbose_name_plural = 'Tables'
            ordering = ['-arrival_time']
