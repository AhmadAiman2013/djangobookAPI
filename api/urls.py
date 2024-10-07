from django.urls import path
from api.views import CreateUserView, MyTokenObtainPairView, BookListCreateView, BookRetrieveUpdateDestroyView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"
urlpatterns = [
     path('user/register/', CreateUserView.as_view(), name='register'),
     path('token/', MyTokenObtainPairView.as_view(), name='get_token'),
     path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
     path('books/', BookListCreateView.as_view(), name='book_list_create'),
     path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='books_details')
]
