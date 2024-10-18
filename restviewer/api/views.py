from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    views,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, CustomUser, Genre, Title

from api.filters import TitleFilterSet
from api.mixins import (
    AdminPermissionViewSet,
    OwnerPermissionViewSet
)
from api.permissions import IsAdmin
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleCreateUpdateSerializer,
    TitleReadOnlySerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ['username']

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,),
            )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data)


class SignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_mail(subject='Code confirmation',
                  message='Your confirmation is: '
                          f'{user.confirmation_code}',
                  from_email=settings.EMAIL_HOST,
                  recipient_list=[user.email],
                  fail_silently=False)
        return Response({'email': user.email, 'username': user.username},
                        status=status.HTTP_200_OK)


class GetTokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(CustomUser, username=username)
        if confirmation_code == user.confirmation_code:
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(AdminPermissionViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(AdminPermissionViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    AdminPermissionViewSet
):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update',):
            return TitleCreateUpdateSerializer
        return TitleReadOnlySerializer


class ReviewViewSet(OwnerPermissionViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(OwnerPermissionViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return get_object_or_404(
            title.reviews.all(), pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
