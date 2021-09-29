from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('projects-list/', views.projectsList, name="projects-list"),
    path('projects-detail/<str:pk>/', views.projectsDetail, name="projects-Detail"),
    path('projects-update/<str:pk>/', views.projectsUpdate, name="projects-update"),
    path('projects-create/', views.projectsCreate, name="projects-Create"),
    path('projects-delete/<str:pk>/', views.projectsDelete, name="projects-delete"),
    path('projects-assign-tradie/', views.assignProject, name="projects-assign-tradie")
  ]