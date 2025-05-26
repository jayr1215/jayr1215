from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title
