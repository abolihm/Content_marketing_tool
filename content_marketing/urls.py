from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from users.views import dashboard

urlpatterns = [
    path('', lambda request: redirect('dashboard/')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-user/', include('users.urls')),
    path('add-existing/', include('projects.urls')), 
    path('user-dashboard/', include('users.urls')),
]
