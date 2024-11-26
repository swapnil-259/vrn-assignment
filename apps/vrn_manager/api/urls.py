from django.urls import  path
from apps.vrn_manager.api.views import EventRegisterView,EventDetailsView,CancelEvent

urlpatterns = [
    path('event/',EventRegisterView.as_view()),
    path('event-details/<int:pk>/',EventDetailsView.as_view()),
    path('cancel-event/<int:pk>/',CancelEvent.as_view()),
    

    
]
