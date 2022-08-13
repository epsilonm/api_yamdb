from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.validators import UniqueValidator


User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=settings.USER_ROLES,
                                   required=False,
                                   )
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all()
                                     )])
    email = serializers.EmailField(required=True,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all()
                                     )])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class UserPatchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all()
                                     )])
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all()
                                   )])
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        extra_kwargs = {'confirmation_code': {'write_only': True}}
        model = User

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        message = (f'Hello, {user.username}! '
                   f'Your confirmation code: {user.confirmation_code}')
        send_mail(message=message,
                  subject='Confirmation code',
                  recipient_list=[user.email],
                  from_email=None
                  )
        return user


class UserJWTTokenCreateSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')
