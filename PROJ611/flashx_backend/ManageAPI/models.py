from django.db import models
from django.contrib.auth.models import User


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


class Store(models.Model):
	store_name = models.CharField(max_length=100)


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=100)


class InvoiceImage(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True, blank=True)