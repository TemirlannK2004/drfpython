
from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from djoser.views import TokenDestroyView
from djoser import views
from djoser.views import UserViewSet,TokenCreateView
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from tutors.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView
)
router = DefaultRouter()
# router.register(r'auth/tutors', CustomTokenObtainPairViewSet, basename='custom_token_obtain_pair')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tutors.urls')),
    path('', include(router.urls)),
    path('auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),

    path('signup/tutor/', UserViewSet.as_view({'post': 'create'}), name='tutor_signup'),
    path('signin/tutor/', CustomTokenObtainPairView.as_view(), name='tutor_signin'),
    

    path('tutors/', TutorsListView.as_view(), name='tutors_list'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('tutor/<int:pk>/',UserProfileView.as_view(), name='tutor_detail_page'),
    path('tutor/<int:pk>/review/', ReviewCreateView.as_view(), name='review_page'),
    # path('auth/tutors/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('auth/token/destroy/', TokenDestroyView.as_view(), name='token-destroy'), 
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)