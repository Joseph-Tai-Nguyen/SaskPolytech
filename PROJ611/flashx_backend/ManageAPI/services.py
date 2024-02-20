from django.conf import settings
from FlashX.utils import upload_file, remove_file, download_file
from . import models, serializers

class ManageServices:
    def create_owner(username, password, email, first_name, last_name, is_admin, is_active, group_name):
        try:
            if is_admin == '' or is_admin == 'false' or is_admin == 'False':
                is_admin = False

            if is_active == '' or is_active == 'false' or is_active == 'False':
                is_active = False

            user = models.User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_superuser=is_admin,
                is_active=is_active,
                is_staff=True
            )
            user.set_password(password)
            user.save()
            group = ManageServices.get_group(name=group_name)
            user.groups.add(group)
            return user
        except Exception as e:
            print(e)
            return None
        
    def update_owner(id, username, email, first_name, last_name, is_admin, is_active, group_name):
        try:
            if is_admin == '' or is_admin == 'false' or is_admin == 'False':
                is_admin = False

            if is_active == '' or is_active == 'false' or is_active == 'False':
                is_active = False

            # get Staff = User
            user = models.User.objects.get(id=id)
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_superuser = is_admin
            user.is_active = is_active

            if group_name == '' or group_name == 'Delivery':
                user.is_staff = False
            else:
                user.is_staff = True

            #user.set_password(password)
            user.save()
            new_group = ManageServices.get_group(name=group_name)
            current_group = user.groups.through.objects.get(user=id)
            current_group.group = new_group
            current_group.save()

            return user
        except Exception as e:
            print(e)
            return None
        
    def create_staff(username, password, email, first_name, last_name, is_active, group_name):
        try:
            is_admin = False
            user = ManageServices.create_owner(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_admin=is_admin,
                is_active=is_active,
                group_name=group_name
            )
            group = ManageServices.get_group(name=group_name)
            user.groups.add(group)
            staff = models.Staff.objects.create(
                user=user
            )
            return staff
        except Exception as e:
            print(e)
            return None

    def create_delivery(username, password, email, first_name, last_name, is_active, group_name):
        try:
            user = models.User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,
                is_active=is_active,
                is_staff=False
            )
            user.set_password(password)
            user.save()
            group = ManageServices.get_group(name=group_name)
            user.groups.add(group)
            delivery = models.Delivery.objects.create(
                user=user
            )
            return delivery
        except Exception as e:
            print(e)
            return None
        
    def get_group(name):
        return models.Group.objects.get(name=name)