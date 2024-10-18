import re

from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, permissions, viewsets

from api.permissions import (
    IsAdmin,
    IsModerator,
    IsOwnerOrReadOnly,
)


class AdminPermissionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly | IsAdmin,
    )
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter
    )


class OwnerPermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly
        | permissions.IsAuthenticated,
        (IsOwnerOrReadOnly | IsAdmin | IsModerator)
    )
    http_method_names = ('get', 'post', 'patch', 'delete')


class UsernameValidate:
    @staticmethod
    def validate_username(username):
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if username == 'me' or not bool(pattern.match(username)):
            raise ValidationError(f'Login {username} unavailable')
        return username
