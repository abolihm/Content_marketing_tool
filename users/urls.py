from django.urls import path
from .views import add_user_view , user_dashboard_view

urlpatterns = [
    path('add-user/', add_user_view, name='add-user'),
    path('user-dashboard/',user_dashboard_view, name='user-dashboard'),
]
