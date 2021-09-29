from django.shortcuts import render
from .models import Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ProjectSerializer, ProjectUpdateSerializer, ProjectCreateSerializer, ProjectTradieSerializer
from rest_framework import status
from tradie.models import Tradie
from django.conf import settings

# Create your views here.


@api_view(['GET'])
@permission_classes((AllowAny, ))
def allapiOverview(request):
    User_API = {
        "All-Users": f"https://{settings.URL}/api/v1/users/",
        'Registration': f"https://{settings.URL}/api/v1/users/register/",
        "Login": f"https://{settings.URL}/api/v1/users/login/",
        "Change-Password": f"https://{settings.URL}/api/v1/users/change-password/",
        "Request_Reset_Email": f"https://{settings.URL}/api/v1/users/request-reset-email/",
        "Password_Reset_Complate": f"https://{settings.URL}/api/v1/users/password-reset-complete/",
        "Current-User": f"https://{settings.URL}/api/v1/users/current-user/",
        
    }
    Project_API = {
        'Project_List': f'https://{settings.URL}/api/v1/projects/projects-list/',
        'Project_Detail View': f'https://{settings.URL}/api/v1/projects/projects-detail/<str:pk>/',
        'Project_Create': f'https://{settings.URL}/api/v1/projects/projects-create/',
        'Project_Update': f'https://{settings.URL}/api/v1/projects/projects-update/<str:pk>/',
        'Project_Delete': f'https://{settings.URL}/api/v1/projects/projects-delete/<str:pk>/',
        'Project_Assign_Tradie': f'https://{settings.URL}/api/v1/projects/projects-assign-tradie/<str:pk>/',
    }
    Tradie_API = {
        'Tradie_List': f'https://{settings.URL}/api/v1/tradie/tradie-list/',
        'Tradie_Detail_View': f'https://{settings.URL}/api/v1/tradie/tradie-detail/<str:pk>/',
        'Tradie_Create': f'https://{settings.URL}/api/v1/tradie/tradie-create/',
        'Tradie_Update': f'https://{settings.URL}/api/v1/tradie/tradie-update/<str:pk>/',
        'Tradie_Delete': f'https://{settings.URL}/api/v1/tradie/tradie-delete/<str:pk>/',
        'Tradie_Change_Status': f'https://{settings.URL}/api/v1/tradie/tradie-update-status/<str:pk>/',
    }
    return Response({"User":User_API,"Projects":Project_API, "Tradies":Tradie_API})


"""
API Overview
"""
@api_view(['GET'])
@permission_classes((AllowAny, ))
def apiOverview(request):
    api_urls = {
        'List': '/projects-list/',
        'Detail View': '/projects-detail/<str:pk>/',
        'Create': '/projects-create/',
        'Update': '/projects-update/<str:pk>/',
        'Delete': '/projects-delete/<str:pk>/',
    }
    return Response(api_urls)


"""
Below Function going to display all the Projects store in the data base.
"""

@api_view(['GET'])
@permission_classes((AllowAny, ))
def projectsList(request):
    try:
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)
    except:
        return Response({"message": "Projects List is empty"}, status=status.HTTP_404_NOT_FOUND)


"""
This Function going to display Detailed view of one perticuler Project with the help of pk.
"""


@api_view(['GET'])
@permission_classes((AllowAny, ))
def projectsDetail(request, pk):
    try:
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)
    except:
        return Response({"message": "This project is no more"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def projectsUpdate(request, pk):
    try:
        task = Project.objects.get(id=pk)
        serializer = ProjectUpdateSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    except:
        return Response({"message": "This project is no more", "status": "false"}, status=status.HTTP_404_NOT_FOUND)


"""
This Function going to Create A new Projects.
"""


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def projectsCreate(request):
    serializer = ProjectCreateSerializer(data=request.data)
    if serializer.is_valid():
        if request.data.get('status') == None:
            return Response({'status': ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        Project.objects.create(project_id=request.data.get('project_id'), address=request.data.get('address'), contact_details=request.data.get(
            'contact_details'), email=request.data.get('email'), phone=request.data.get('phone'), plans=request.data.get('plans'), status=request.data.get('status'), file=request.FILES['file'], user=request.user)
        return Response({"message": "Successfully create new project", "status": "true"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def projectsDelete(request, pk):
    try:
        project = Project.objects.get(id=pk)
        project.delete()
        return Response({"message": "Project deleted successfully."}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "This project is no more", "status": "false"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def assignProject(request):
    try:
        serializer = ProjectTradieSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Project.objects.get(id=request.data.get('project_id'))
                try:
                    Tradie.objects.get(id=request.data.get('tradie_id'))
                    serializer.save()
                    return Response({"message": "Project Assign successfully."}, status=status.HTTP_200_OK)
                except:
                    return Response({"message": "This Tradie is not found", "status": "false"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({"message": "This project is not found", "status": "false"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "This project is no more", "status": "false"}, status=status.HTTP_404_NOT_FOUND)
