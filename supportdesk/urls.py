from django.urls import path

from . import views

urlpatterns = [
    path("customer/requests", views.CustomerRequests.as_view(), name="supportdesk_customer_requests", ),
    path("customer/create-ticket", views.CustomerCreateTicket.as_view(), name="supportdesk_create_ticket", ),
    path("agent/requests", views.AgentRequests.as_view(), name="supportdesk_agent_requests", ),
    path("agent/view-request/<int:pk>", views.AgentViewRequest.as_view(), name="supportdesk_agent_view_request", ),
    path("agent/reassign/<int:pk>", views.AgentReAssignRequest.as_view(), name="supportdesk_agent_reassign_request", ),
]
