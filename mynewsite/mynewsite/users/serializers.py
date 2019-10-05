from rest_framework import serializers

from mynewsite.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        fields = ('email', 'password', 'first_name', 'last_name')

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        ret.pop('password')
        return ret

class UserUnauthorizedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        fields = ('first_name',)


