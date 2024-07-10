from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('user_search/', UserSearchView.as_view()),
    path('user_name_check/', CheckUsernameView.as_view()),
    path('retrieve/', RetrieveProfileView.as_view()),
    path('user_list/', UserListView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
