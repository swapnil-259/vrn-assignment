from django.urls import  path
from apps.vrn_user.api.views import RegisterEventView,CancelRegistrationView

urlpatterns = [
    path('register-event/',RegisterEventView.as_view()),
    path('cancel-registration/<int:pk>/',CancelRegistrationView.as_view())
    

    
]
