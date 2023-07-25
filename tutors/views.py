from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import TutorFilter


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(response.data, status=201)

class TutorsListView(generics.ListAPIView):
    queryset = TutorUser.objects.all()
    serializer_class = TutorListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TutorFilter
    def get_queryset(self):
        return TutorUser.objects.filter(activate_post=True)

class UserProfileView(generics.RetrieveAPIView):
    queryset = TutorUser.objects.all()
    serializer_class = TutorUserProfile
    lookup_field = 'pk'


class UpdateProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorUser.objects.all()
    serializer_class = UpdateUserSerializer




class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom URL for SignIn Tutor JWT"""
    serializer_class = CustomTokenObtainPairSerializer

# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()  
#             return Response({"message": "Logout successful."}, status=200)
#         except Exception as e:
#             return Response({"error": "Invalid token."}, status=400)


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
#     permission_classes = [permissions.AllowAny]


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#         token['email'] = user.email
#         token['first_name'] = user.first_name
#         token['last_name'] = user.last_name
#         return token

# class CustomTokenObtainPairView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = MyTokenObtainPairSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.user
#         refresh = RefreshToken.for_user(user)
#         token_data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#         return Response(token_data)

# class CustomTokenObtainPairViewSet(ViewSet):
#     permission_classes = [AllowAny]

#     @action(detail=False, methods=['post'])
#     def login(self, request):
#         view = CustomTokenObtainPairView.as_view()
#         return view(request._request)