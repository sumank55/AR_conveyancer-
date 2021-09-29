from django.urls import path
from . import views


urlpatterns = [
    path('', views.apiOverviewTradie, name="api-overview"),
    path('tradie-list/', views.tradieList, name="tradie-list"),
    path('tradie-detail/<str:pk>/', views.tradieDetail, name="tradie-Detail"),
    path('tradie-update/<str:pk>/', views.tradieUpdate, name="tradie-update"),
    path('tradie-create/', views.tradieCreate, name="tradie-Create"),
    path('tradie-delete/<str:pk>/', views.tradieDelete, name="tradie-delete"),
    path('tradie-update-status/<str:pk>/', views.tradieStatusUpdate, name="tradie-update-status"),
    
  ]