from rest_framework import generics
from api.models import CustomUser, Books
from .serializers import UserSerializer, MyTokenObtainPairSerializer, BooksSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAuthor
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        serializer.save()
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
            'page_size': self.page.paginator.per_page,
            'total_pages': self.page.paginator.num_pages,
            'total_items': self.page.paginator.count,  
            'next': self.get_next_link(), 
            'previous': self.get_previous_link(),  
            'results': data  
        })
    
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter
    pagination_class = BookPagination
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            raise NotFound({"detail": "No books exist for the specified criteria."})
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthor]
    
   
