from api.models import CustomUser
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