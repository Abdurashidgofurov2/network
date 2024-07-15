from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from . import models
from .models import User
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from .utils import unhash_token



class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        # Check if the username is already taken
        if User.objects.filter(username=data.get('username')).exists():
            raise ValidationError({'username': 'This username is already taken'})



        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the newly registered user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        token_data = {
            "refresh": str(refresh),
            "access": str(access_token),
        }

        return Response(token_data, status=status.HTTP_201_CREATED)





class UserSearchView(generics.ListAPIView):

    serializer_class = UserProfileSerializer


    search_param = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description="Search users by username or email",
        type=openapi.TYPE_STRING,
        required=True
    )

    @swagger_auto_schema(manual_parameters=[search_param])
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search')
        if not search_query:
            raise ValidationError(_("The 'search' parameter is required."))

        users = User.objects.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CheckUsernameView(generics.GenericAPIView):
    serializer_class = CheckUsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Username is available'}, status=status.HTTP_200_OK)



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer



class RetrieveProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')

        if not user_id:
            raise NotFound("User not found")

        user = get_object_or_404(User, id=user_id)
        serializer = self.get_serializer(user)

        return Response(serializer.data)