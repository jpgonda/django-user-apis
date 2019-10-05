# from django.core.mail import send_mail

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action

from mynewsite.users.models import User, AuthToken
from mynewsite.users.serializers import UserSerializer, UserUnauthorizedSerializer


class CustomRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            # TODO: create emailer account to be able to send email from django
            # object = serializer.save()
            # token = Token.objects.get(user=object)
            # send_mail(
            #     'Token for Activation',
            #     'Here is your token %s' %token,
            #     'from@gmail.com',
            #     ['%s' %object.email],
            #     fail_silently=False,
            # )
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def list(self, request):
        token = request.headers['Authorization'].replace('Bearer ', '')
        try:
            Token.objects.get(key=token)
            return Response(data=self.get_serializer(self.queryset, many=True).data)
        except Exception:
            return Response(data=UserUnauthorizedSerializer(self.queryset, many=True).data)

    @action(methods=['PUT'], detail=False, url_path='key')
    def activate(self, request, pk=None):
        token = request.data.get('token')
        user = self.queryset.filter(auth_token__key=token).first()
        if user:
            user.is_active = True
            user.save()
            return Response(data=self.get_serializer(user).data)
        else:
            return Response(data={'error': "Token is invalid"}, status=404)

    @action(methods=['PUT'], detail=False, url_path='password')
    def change_password(self, request):
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        token = request.headers['Authorization'].replace('Bearer ', '')
        try:
            user = self.queryset.get(auth_token__key=token)
            try:
                user.check_password(password)
                user.set_password(new_password)
                user.save()
                return Response(data=self.get_serializer(user).data)
            except Exception:
                return Response(data={'error': 'Invalid username or password'}, status=401)
        except Exception:
            return Response(data={'error': 'Token is Invalid'}, status=404)


class CustomAuthToken(ObtainAuthToken):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })