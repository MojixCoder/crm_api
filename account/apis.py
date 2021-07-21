from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt import exceptions

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

from .models import User
from .serializers import UserRetrieveSerializer, UserListSerializer, UserCreateSerializer, UserUpdateSerializer


@extend_schema_view(
    list=extend_schema(
        description='Retrieve users',
        methods=["GET"],
        responses={
            201: UserCreateSerializer,
            404: OpenApiResponse(response=dict, description='Invalid page.',),
        },
        parameters=[
            OpenApiParameter("page", OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
        ],
    ),
    create=extend_schema(
        description='Create a user',
        methods=["POST"],
        responses={
            201: UserCreateSerializer,
            400: OpenApiResponse(response=dict, description='Validation error.',),
        },
        request=UserCreateSerializer,
    ),
    retrieve=extend_schema(
        description='Retrieve a user',
        methods=["GET"],
        responses={
            200: UserRetrieveSerializer,
            404: OpenApiResponse(response=dict, description='User not found.',),
        },
        parameters=[
            OpenApiParameter("username", OpenApiTypes.STR, OpenApiParameter.PATH),
        ],
    ),
    update=extend_schema(
        description='Update a user',
        methods=["PUT"],
        responses={
            200: UserUpdateSerializer,
            400: OpenApiResponse(response=dict, description='Validation error.',),
        },
        parameters=[
            OpenApiParameter("username", OpenApiTypes.STR, OpenApiParameter.PATH),
        ],
    ),
    token=extend_schema(
        description='Obtain pair token',
        methods=["POST"],
        responses={
            200: TokenObtainPairSerializer,
            400: OpenApiResponse(response=dict, description='Validation error.',),
            401: OpenApiResponse(response=dict, description='Wrong username or password.',),
        },
    ),
    refresh_token=extend_schema(
        description='Get access token by refresh token',
        methods=["POST"],
        responses={
            200: TokenRefreshSerializer,
            400: OpenApiResponse(response=dict, description='Validation error.',),
            401: OpenApiResponse(response=dict, description='Token is invalid or expired.',),
        },
    ),
)
class UserViewSet(ModelViewSet):
    """ User Model View Set """
    
    queryset = User.objects.all()
    http_method_names = ["get", "put", "post",]
    lookup_field = "username"
    # permission_classes = [AllowAny,]
    lookup_url_kwarg = "username"
    
    def get_serializer_class(self):
        
        if self.action == "list":
            return UserListSerializer
        elif self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "create":
            return UserCreateSerializer
        elif self.action == "update":
            return UserUpdateSerializer
        elif self.action == "token":
            return TokenObtainPairSerializer
        elif self.action == "refresh_token":
            return TokenRefreshSerializer
        
        return UserListSerializer
    
    def get_object(self):
        username = self.kwargs[self.lookup_url_kwarg]
        try:
            user = User.objects.prefetch_related("permissions").get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, obj=user)
        return user
    
    @action(
        methods=["post",], 
        detail=False, 
        name="Obtain pair token", 
        url_name="token_obtain_pair", 
        permission_classes=[AllowAny], 
    )
    def token(self, request, *args, **kwargs):
        """ Get access token """
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    @action(
        methods=["post",], 
        detail=False, 
        name="Refresh token", 
        url_name="token_refresh", 
        url_path="token/refresh",
        permission_classes=[AllowAny], 
    )
    def refresh_token(self, request, *args, **kwargs):
        """ Get refresh token """
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    