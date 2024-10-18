import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import year_validator
from api.mixins import UsernameValidate

from api.variable import LIMIT_NAME_LENGTH, LIMIT_EMAIL_LENGTH


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )

    username = models.CharField(
        'username',
        max_length=LIMIT_NAME_LENGTH,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[UsernameValidate.validate_username],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    bio = models.TextField('Bio', blank=True, null=True)
    email = models.EmailField('email address',
                              max_length=LIMIT_EMAIL_LENGTH,
                              unique=True,
                              blank=False)
    role = models.CharField('User_role', max_length=100,
                            choices=ROLE_CHOICES,
                            default='user')
    confirmation_code = models.CharField(max_length=70,
                                         unique=True,
                                         blank=True,
                                         null=True,
                                         default=uuid.uuid4)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_admin

    class Meta:
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


class NameSlugModel(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True
    )


class Category(NameSlugModel):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(NameSlugModel):

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=256
    )
    year = models.SmallIntegerField(
        verbose_name='Year',
        validators=(
            year_validator,
        ),
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class AuthorTextPubDateModel(models.Model):
    text = models.TextField('Text')
    pub_date = models.DateTimeField(
        'Published date', auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='User')

    class Meta:
        abstract = True


class Review(AuthorTextPubDateModel):
    score = models.PositiveSmallIntegerField('Score')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Title')

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title')
        ]

    def __str__(self):
        return f'{self.author} rated {self.title}'


class Comment(AuthorTextPubDateModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Review')

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'comments'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.author} comments "{self.review}"'
