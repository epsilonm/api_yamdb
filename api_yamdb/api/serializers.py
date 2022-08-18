from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comment
from .validators import UserNameValidator

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
        validators = [UserNameValidator]
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
        validators = [UserNameValidator]
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        validators = [UserNameValidator]
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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitlesReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlesEditorSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title, author=request.user).exists():
                raise ValidationError('Можно оставлять только один'
                                      'отзыв на произведение.')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
