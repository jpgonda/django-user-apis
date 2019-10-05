from rest_framework import viewsets
from mynewsite.users.models import User, AuthToken
from mynewsite.users.serializers import CustomUserDetailsSerializer, CustomUserDetailsUnauthorizedSerializer
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action


class CustomRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserDetailsSerializer

    def create(self, request):
        serializer = CustomUserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            object = serializer.save()
            token = Token.objects.get(user=object)
            print(token.user)
            print(object.email)
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
        # import pdb; pdb.set_trace()
        token = request.headers['Authorization'].replace('Bearer ', '')
        try:
            Token.objects.get(key=token)
            return Response(data=self.get_serializer(self.queryset, many=True).data)
        except Exception:
            return Response(data=CustomUserDetailsUnauthorizedSerializer(self.queryset, many=True).data)

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

        # user = self.queryset.get(email=email)
        # if user:
        #     try:
        #         validate_password(password, user)
        #
        #     except ValidationError:
        #         return Response(data={'error': 'Invalid username or password'}, status=401)
        #
        # else:
        #     return Response(data={'error': "Token is invalid"}, status=404)


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