from django.urls import path
from .views import add_project_view, add_in_existing_project_view , not_permission_view

urlpatterns = [
    path('add-new/', add_project_view, name='add-project'),
    path('add-existing/', add_in_existing_project_view, name='add-in-existing-project'),
    path('no_permission/',not_permission_view, name='not_permission'),
]
