#LOGIN AUTH
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        #add custom claims
        token['username'] = user.username
        return token

#SIGNUP AUTH
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model=User
        fields = ['username','password','email',]