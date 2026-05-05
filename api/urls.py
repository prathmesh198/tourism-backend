from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, forecast_tourists, LogoutView, RegisterView, CustomAuthToken

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('forecast/', forecast_tourists, name='forecast'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_logout'),
]
