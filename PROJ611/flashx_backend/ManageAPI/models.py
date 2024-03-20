from django.db import models
from django.contrib.auth.models import User, Group
from .enums import InvoiceStatus


class Base(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(Base):
    unique_name = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)


class Store(Base):
    store_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True)


class Store_Staff(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class InvoiceChoices(models.TextChoices):
    CREATED = InvoiceStatus.CREATED.value, 'created'
    WAITING = InvoiceStatus.WAITING.value, 'waiting'
    DELIVERING = InvoiceStatus.DELIVERING.value, 'delivering'
    COMPLETED = InvoiceStatus.COMPLETED.value, 'completed'
    CANCELED = InvoiceStatus.CANCELED.value, 'canceled'


class Invoice(Base):
    invoice_no = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_creator')
    courier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='invoice_courier')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=InvoiceChoices.choices, default=InvoiceChoices.CREATED)
    inv_images = models.ManyToManyField(Image, null=True, blank=True, related_name='invoice_images')
    evi_images = models.ManyToManyField(Image, null=True, blank=True, related_name='evidence_images')


# class InvoiceImage(Base):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     invoice_image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True, related_name='invoice_image')
#     evidence_image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True, related_name='evidence_image')