from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Delivery, Staff, Invoice, Image, Store, Store_Staff


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ['permissions']


class OwnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.SlugRelatedField(many=True, queryset=Group.objects.all(), slug_field='name')
    class Meta:
        model = User
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    user = OwnerSerializer()
    class Meta:
        model = Staff
        #fields = ['user']
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    user = OwnerSerializer()
    class Meta:
        model = Delivery
        #fields = ['user']
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

class StoreStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store_Staff
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


# class InvoiceImageSerializer(serializers.ModelSerializer):
#     image = ImageSerializer()
#     class Meta:
#         model = InvoiceImage
#         fields = "__all__"

