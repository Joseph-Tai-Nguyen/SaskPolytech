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
      GroupSerializer, ImageSerializer, StoreSerializer, StoreStaffSerializer
from .models import Staff, Delivery, Invoice, Image, Store, Store_Staff
from . import services, permissions
from django.http import HttpResponse


@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        user.last_login = timezone.datetime.now()
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
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAdmin]
    serializer_class = OwnerSerializer
    queryset =  User.objects.all().filter(is_staff=True)
    
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

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            result = services.ManageServices.create_staff(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_active=data['is_active'],
                group_name=data['group']
            )
            if result is not None:
                return Response({'status': 'New staff has been added'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Cannot create new staff'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('EXCEPTION')
            print(e)
            return Response({'error': 'Cannot create new staff'}, status=500)

    def update(self, request, *args, **kwargs):
        data = request.data
        staffid = kwargs['pk']

        result = services.ManageServices.update_staff_delivery(
            id=staffid,
            username=data['username'],
            # password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_active=data['is_active'],
            group_name=data['group'],
            is_staff=True
        )

        if result is not None:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Fail to update tutor.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        staffid = kwargs['pk']
        # get Staff
        staff = Staff.objects.get(id=staffid)

        # delete user
        # delete cascade Staff
        staff.user.delete()

        return Response({'status': 'Staff deleted'}, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    # def tutor_dashboard(self, request):
    #     try:
    #         user = request.user
    #         tutor = Tutor.objects.get(user=user)
    #         courses_list = Course.objects.filter(tutor=tutor)
    #         events = SearchService.find_event_by_host(tutor)
    #         response = {
    #             'tutor': user.first_name + ' ' + user.last_name,
    #             'tutor_id': tutor.id,
    #             'num_courses': len(courses_list),
    #             'num_events': len(events),
    #             'num_students': len(courses_list)
    #         }

    #         return Response(response, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)
    #         return Response(status=400)

    def list(self, request, *args, **kwargs):
        response = []

        # get list Staff
        staff_list = Staff.objects.all()
        for staff in staff_list:
            user = staff.user
            group = GroupSerializer(user.groups.filter(user=user), many=True).data

            if len(group) > 0:
                dictionary = {
                    'staffid': staff.id,
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
                    'staffid': staff.id,
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
        staffid = kwargs['pk']
        # get Staff
        staff = Staff.objects.get(id=staffid)
        user = staff.user
        group = GroupSerializer(user.groups.filter(user=user), many=True).data

        if len(group) > 0:
            return Response({
                'staffid': staff.id,
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
                'staffid': staff.id,
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


class DeliveryViewSet(ModelViewSet):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data

        result = services.ManageServices.create_delivery(
            username=data['email'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_active=data['is_active'],
            group_name=data['group']
        )
        if result is not None:
            return Response({'status': 'New delivery has been added'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Cannot create new delivery'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        deliveryid = kwargs['pk']

        result = services.ManageServices.update_staff_delivery(
            id=deliveryid,
            username=data['email'],
            # password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_active=data['is_active'],
            group_name=data['group'],
            is_staff=False
        )

        if result is not None:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Fail to update delivery.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        deliveryid = kwargs['pk']

        # get Delivery
        delivery = Delivery.objects.get(id=deliveryid)
        # # get User
        # user = User.objects.get(id=delivery.user.id)
        # # delete Delivery
        # delivery.delete()
        # # delete user
        # user.delete()

        # delete user
        # delete cascade Delivery
        delivery.user.delete()

        return Response({'status': 'Student deleted'}, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    # def courses(self, request):
    #     user = request.user
    #     student = Student.objects.get(user=user)
    #     courses_students = CourseStudent.objects.filter(student=student)
    #     courses = []
    #     for cs in courses_students:
    #         courses.append(cs.course)
    #     serializer = CourseSerializer(courses, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    # def student_dashboard(self, request):
    #     try:
    #         user = request.user
    #         student = Student.objects.get(user=user)

    #         courses = CourseStudent.objects.filter(student=student)
    #         events = SearchService.find_event_by_participant(student)
    #         response = {
    #             'student': user.first_name + ' ' + user.last_name,
    #             'num_tutors': len(courses),
    #             'num_courses': len(courses),
    #             'num_events': len(events)
    #         }
    #         return Response(response, status=200)

    #     except Exception as e:
    #         print(e)
    #         return Response(status=500)

    def list(self, request, *args, **kwargs):
        response = []

        # get list Delivery
        delivery_list = Delivery.objects.all()
        for delivery in delivery_list:
            user = delivery.user
            group = GroupSerializer(user.groups.filter(user=user), many=True).data

            if len(group) > 0:
                dictionary = {
                    'deliveryid': delivery.id,
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
                    'deliveryid': delivery.id,
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
        deliveryid = kwargs['pk']
        # get Delivery
        delivery = Delivery.objects.get(id = deliveryid)
        user = delivery.user
        group = GroupSerializer(user.groups.filter(user=user), many=True).data

        if len(group) > 0:
            return Response({
                'deliveryid': delivery.id,
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
                'deliveryid': delivery.id,
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

class GroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class InvoiceViewSet(ModelViewSet):
    permissions_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


class StoreViewSet(ModelViewSet):
    permissions_classes = [IsAuthenticated]
    serializer_class = StoreSerializer
    queryset = Store.objects.all()

    def create(self, request, *args, **kwargs):
        new_store = services.ManageServices.create_store(request.data)
        if new_store is not None:
            print(new_store)
            return Response(
                {'store': new_store.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'Store creation failed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
