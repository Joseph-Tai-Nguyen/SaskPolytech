from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from ManageAPI import services
from .serializers import OwnerSerializer, DeliverySerializer, InvoiceSerializer, StaffSerializer, \
      GroupSerializer, ImageSerializer, InvoiceImageSerializer, StoreSerializer
from .models import Staff, Delivery, Invoice, InvoiceImage, Image, Store
from . import services, permissions
from django.http import HttpResponse


@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        user.last_login = timezone.now
        user.save()
        token, obj = Token.objects.get_or_create(user=user)
        group = GroupSerializer(user.groups.filter(user=user), many=True).data

        if len(group) > 0:
            return Response({
                'token': token.key,
                'groups': group[0]['name'],
                'user': {
                    "id": user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'token': token.key,
                'groups': 'admin',
                'user': {
                    "id": user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined
                }
            }, status=status.HTTP_200_OK)

    else:
        return Response({'error': "User not found."}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def logout(request):
    try:
        id = request.query_params.get('id', None)
        if id is not None:
            user = User.objects.get(id=id)
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'result': 'Logout'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'Exception'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def set_password(request):
    try:
        new_password = request.data['new_pass']
        if not request.user.check_password(new_password):
            request.user.set_password(new_password)
            request.user.save()
            return Response({'status': 'Password successfully updated'}, status=200)
        else:
            return Response({'status': 'New password must not match old password'}, status=400)
    except Exception as e:
        print(e)
        return Response({'status': 'Internal server error'}, status=500)


class OwnerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OwnerSerializer
    queryset = User.objects.all().filter(is_staff=True)

    def create(self, request, *args, **kwargs):
        data = request.data

        result = services.ManageServices.create_owner(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=data['is_admin'],
            is_active=data['is_active'],
            group_name=data['group']
        )

        if result is not None:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Fail to create owner.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        ownerid = kwargs['pk']

        result = services.ManageServices.update_owner(
            id=ownerid,
            username=data['username'],
            # password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=data['is_admin'],
            is_active=data['is_active'],
            group_name=data['group']
        )

        if result is not None:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Fail to update owner.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def details(self, request, pk=None):
        user_data = request.user
        user = self.serializer_class(instance=user_data)
        return Response(
            {
                'details': user.data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        user_data = request.user
        return super(OwnerViewSet, self).destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = []

        # get list Owner
        user_list = User.objects.filter(is_staff=True)
        for user in user_list:
            group = GroupSerializer(user.groups.filter(user=user), many=True).data

            if len(group) > 0:
                dictionary = {
                    'groups': group[0]['name'],
                    'user': {
                        "id": user.id,
                        "last_login": user.last_login,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_active': user.is_active,
                        'date_joined': user.date_joined
                    }
                }
            else:
                dictionary = {
                    'groups': 'no group',
                    'user': {
                        "id": user.id,
                        "last_login": user.last_login,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_active': user.is_active,
                        'date_joined': user.date_joined
                    }
                }
            response.append(dictionary)

        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        ownerid = kwargs['pk']
        user = User.objects.get(id=ownerid)
        group = GroupSerializer(user.groups.filter(user=user), many=True).data

        if len(group) > 0:
            return Response({
                'groups': group[0]['name'],
                'user': {
                    "id": user.id,
                    "last_login": user.last_login,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'groups': 'no group',
                'user': {
                    "id": user.id,
                    "last_login": user.last_login,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined
                }
            }, status=status.HTTP_200_OK)


class StaffViewSet(ModelViewSet):
    permission_classes = [permissions.IsStaff]
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()


class DeliveryViewSet(ModelViewSet):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class InvoiceViewSet(ModelViewSet):
    permission_classes = [permissions.IsStaff]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def destroy(self, request, *args, **kwargs):
        invoiceid = kwargs['pk']
        # get list Course
        invoice_images = InvoiceImage.objects.filter(invoice_id=invoiceid)

        for image in invoice_images:
            # delete Invoice Image
            image.delete()

        # get Invoice
        invoice = Invoice.objects.get(id=invoiceid)
        # delete Invoice
        invoice.delete()

        return Response({'status': 'Invoice deleted'}, status=status.HTTP_200_OK)