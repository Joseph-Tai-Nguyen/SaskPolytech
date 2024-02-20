from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet, obtain_auth_token, login, logout, GroupViewSet, OwnerViewSet, DeliveryViewSet, InvoiceViewSet, set_password


router = DefaultRouter()
router.register(r'group', GroupViewSet, basename='group')
router.register(r'owner', OwnerViewSet, basename='owner')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'delivery', DeliveryViewSet, basename='delivery')
router.register(r'invoice', InvoiceViewSet, basename='invoice')


urlpatterns = [
    path('', include(router.urls)),
    path('token-auth', obtain_auth_token, name='token_auth'),
    path('login', login),
    path('logout', logout),
    path('set_pass', set_password)
    # path('view_dashboard', view_dashboard),
    # path('upload', upload),
    # path('download', download)
]