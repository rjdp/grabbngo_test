from django.db import models
from django.contrib.postgres.fields import JSONField

class BaseTable(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StoreCategory(BaseTable):
    name = models.CharField(max_length=75)
    key = models.CharField(max_length=75)
    uuid = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Store(BaseTable):
    INR = 'INR'
    USD = 'USD'
    CURRENCY_CHOICES = (
        (INR, 'Indian Rupee'),
        (USD, 'US Dollars'))

    uuid = models.CharField(max_length=75, db_index=True)
    title = models.CharField(max_length=75)
    hero_image_url = models.URLField(max_length=300)
    location = JSONField()
    city = models.CharField(max_length=50)
    categories = models.ManyToManyField(StoreCategory)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default=INR,
    )

    def __str__(self):
        return self.title

class Item(BaseTable):
    title = models.CharField(max_length=75)
    image_url = models.URLField(max_length=300, blank=True)
    description = models.CharField(max_length=300, blank=True)
    uuid = models.CharField(max_length=75)
    price =  models.DecimalField(max_digits=8, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    