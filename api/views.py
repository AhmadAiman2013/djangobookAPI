from rest_framework import generics
from rest_framework.request import Request
from api.models import CustomUser, Books
from .serializers import UserSerializer, MyTokenObtainPairSerializer, BooksSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAuthor
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError({"error": "Failed to register: " + str(e)})
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request: Request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            raise ValidationError({"error": "Invalid credentials: " + str(e)})
        except Exception as e:
            raise ValidationError({"error": "An error occurred while obtaining tokens: " + str(e)})

class BookBaseViewUser:
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated]

class BookFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre', lookup_expr='icontains')
    
    class Meta:
        model = Books
        fields = ['genre']

class BookPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response({
            'page_number': self.page.number,
            'page_size': self.page.size,
            'total_pages': self.page.paginator.num_pages,
            'total_items': self.page.paginator.count,  
            'next': self.get_next_link(), 
            'previous': self.get_previous_link(),  
            'results': data  
        })
    
class BookListCreateView(BookBaseViewUser, generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter
    pagination_class = BookPagination
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            raise NotFound({"error" : "Books not found"})
        
    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError({"error": "Failed to create book " + str(e)})

class BookRetrieveView(BookBaseViewUser, generics.RetrieveAPIView):
     def get_object(self):
        try:
            super().get_object()
        except Exception as e:
            raise NotFound({"error" : "Book not found"})
    
class BookUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthor]
    
    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError({"error": "Failed to update book " + str(e)})
        
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except Exception as e:
            raise ValidationError({"error": "Failed to delete book " + str(e)})
