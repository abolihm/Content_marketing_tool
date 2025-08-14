from django.urls import path
from .views import add_user_view , user_dashboard_view , no_permission_view,publication_list_view

urlpatterns = [
    path('add-user/', add_user_view, name='add-user'),
    path('user-dashboard/',user_dashboard_view, name='user-dashboard'),
    path('no_permission/',no_permission_view, name='no_permission'),
    path('/',publication_list_view, name='publication_list'),
]
