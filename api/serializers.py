from api.models import CustomUser, Books
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'password']
        extra_kwargs = {'password' : {'write_only' : True}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['role'] = user.role
        
        return token

class BooksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Books
        fields = ['id', 'title', 'author', 'description', 'price', 'genre', 'publication_date']
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        
        allowed_fields = ['title', 'description', 'price']
        
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
        instance.save()
        
        return instance