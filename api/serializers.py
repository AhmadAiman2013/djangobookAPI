from api.models import CustomUser, Books
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError


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
    author = serializers.CharField(required=False, allow_blank = True)
    genre = serializers.CharField(required=False, allow_blank = True)
    publication_date = serializers.DateField(required=False, allow_null = True)

    class Meta:
        model = Books
        fields = ['id', 'title', 'author', 'description', 'price', 'genre', 'publication_date']

    def validate(self, data):
        
        required_fields = ['title', 'price', 'description']
        request = self.context['request'].method
        
        if request == "POST":
            required_fields.extend(['author', 'genre', 'publication_date'])
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValidationError(f"Insufficient data received: {', '.join(missing_fields)} are required")
        
        return data
    
    def create(self, validated_data):
        return Books.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance