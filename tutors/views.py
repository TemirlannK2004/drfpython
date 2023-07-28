from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import F


from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .permissions import *
from .service import TutorFilter


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken




class ReviewCreateView(generics.CreateAPIView):
    """ Create Review for a Tutor """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(response.data, status=201)

class TutorsListView(generics.ListAPIView):
    """Display All Active Tutors with filter by salary,experience,degree,average rating and courses """
    queryset = TutorUser.objects.all()
    serializer_class = TutorListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TutorFilter
    def get_queryset(self):
        return TutorUser.objects.filter(activate_post=True).annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')

class UserProfileView(generics.RetrieveAPIView):
    """ Display Tutor Profile for Client """
    queryset = TutorUser.objects.all()
    serializer_class = TutorUserProfile
    permission_classes = [IsAuthenticatedOrReadOnly,]
    lookup_field = 'pk'
   


class UpdateProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Update Profile API"""
    queryset = TutorUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes =[IsOwnerOrReadOnly,]


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom URL for SignIn Tutor JWT"""
    serializer_class = CustomTokenObtainPairSerializer





class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = ClientUserProfileSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = ClientUser.objects.get(email=request.user.email)
        user.avatar = request.data['avatar']
        user.save()
        return Response({'message': 'Image updated'}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        # if email is already in use
        if ClientUser.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ClientUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = ClientUser.objects.all()
        serializer = ClientUserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



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