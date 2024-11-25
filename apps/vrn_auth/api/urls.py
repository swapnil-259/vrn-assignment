from django.urls import  path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.vrn_auth.api.views import RegisterUser,RegisterManager

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    path('user/',RegisterUser.as_view()),
    path('manager/',RegisterManager.as_view())

]
