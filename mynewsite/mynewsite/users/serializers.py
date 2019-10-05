# from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from mynewsite.users.models import User
from rest_framework.authentication import TokenAuthentication

class CustomRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('first_name', '')
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        fields = ('email', 'password', 'first_name', 'last_name')

    def to_representation(self, instance):
        ret = super(CustomUserDetailsSerializer, self).to_representation(instance)
        ret.pop('password')
        return ret

class CustomUserDetailsUnauthorizedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        fields = ('first_name',)


