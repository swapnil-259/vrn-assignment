from django.urls import  path
from apps.vrn_manager.api.views import EventRegisterView,CancelEvent

urlpatterns = [
    path('event/',EventRegisterView.as_view()),
    path('cancel-event/<int:pk>/',CancelEvent.as_view()),
    

    
]
