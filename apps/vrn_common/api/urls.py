from django.urls import  path
from apps.vrn_common.api.views import AllOrganizationView,EventOrganizationWise,EventDetailsView,GetAllRegistrationsView
urlpatterns = [
    path('get-organizations/',AllOrganizationView.as_view()),
    path('get-events/<int:pk>/',EventOrganizationWise.as_view()),
    path('event-details/<int:pk>/',EventDetailsView.as_view()),
    path('get-registrations/<int:pk>/',GetAllRegistrationsView.as_view())

    
]
