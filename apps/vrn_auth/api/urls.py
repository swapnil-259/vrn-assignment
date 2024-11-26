from django.urls import  path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.vrn_auth.api.views import RegisterUser,RegisterManager,LogoutView,GetAllUsers,GetAllManagers

urlpatterns = [
    path('login/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    path('user/',RegisterUser.as_view()),
    path('manager/',RegisterManager.as_view()),
    path('logout/',LogoutView.as_view()),
    path('get-all-users/',GetAllUsers.as_view()),
    path('get-all-managers/',GetAllManagers.as_view())



]
