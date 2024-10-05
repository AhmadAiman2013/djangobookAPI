from django.urls import path
from api.views import CreateUserView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"
urlpatterns = [
     path('user/register/', CreateUserView.as_view(), name='register'),
     path('token/', MyTokenObtainPairView.as_view(), name='get_token'),
     path('token/refresh', TokenRefreshView.as_view(), name='refresh')
]
