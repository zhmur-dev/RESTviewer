from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (
    Category,
    Comment,
    CustomUser,
    Genre,
    Review,
    Title
)
from .mixins import UsernameValidate
from .variable import LIMIT_NAME_LENGTH, LIMIT_EMAIL_LENGTH


class UserSerializer(serializers.ModelSerializer, UsernameValidate):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class SignUpSerializer(serializers.Serializer, UsernameValidate):

    email = serializers.EmailField(max_length=LIMIT_EMAIL_LENGTH)
    username = serializers.CharField(
        max_length=LIMIT_NAME_LENGTH,
        validators=[UsernameValidate.validate_username])

    def validate(self, data):
        if not data['username'] or not data['email']:
            raise serializers.ValidationError(
                'Username / e-mail not specified.')
        user = CustomUser.objects.filter(email=data['email']).first()
        if (user and user.email == data['email']
                and user.username != data['username']):
            raise serializers.ValidationError(
                f'E-mail {data["email"]} already exists.')
        user = CustomUser.objects.filter(username=data['username']).first()
        if (user and user.email != data['email']
                and user.username == data['username']):
            raise serializers.ValidationError(
                f'User {data["username"]} already exists.')
        return data

    def create(self, validated_data):
        user = CustomUser.objects.filter(
            username=validated_data['username'],
            email=validated_data['email']
        ).first()
        if not user:
            user = CustomUser.objects.create(**validated_data)
        return user


class GetTokenSerializer(serializers.Serializer, UsernameValidate):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )
    rating = serializers.IntegerField(
        read_only=True,
        default=None
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre'
        )


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        read_only=True,
        default=None
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )
        model = Title


class BaseAuthorSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )


class ReviewSerializer(BaseAuthorSerializer):
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        exclude = ('title',)

    def validate_author(self, value):
        if self.context['request'].method == 'POST':
            request = self.context['request']
            title_id = request.parser_context['kwargs']['title_id']
            title = get_object_or_404(Title, pk=title_id)
            if title.reviews.filter(author__username=value):
                raise serializers.ValidationError(
                    'You can only post one review per title.')
        return value


class CommentSerializer(BaseAuthorSerializer):

    class Meta:
        model = Comment
        exclude = ('review',)
