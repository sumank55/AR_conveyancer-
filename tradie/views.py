from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TradieSerializer, TradieUpdateSerializer, TradieCreatreSerializer
from .models import Tradie
from rest_framework import status


"""
API Overview
"""
@api_view(['GET'])
def apiOverviewTradie(request):
    api_urls = {
        'List': '/tradie-list/',
        'Detail View': '/tradie-detail/<str:pk>/',
        'Create': '/tradie-create/',
        'Update': '/tradie-update/<str:pk>/',
        'Delete': '/tradie-delete/<str:pk>/',
    }
    return Response(api_urls)


"""
Below Function going to display all the Tradies store in the data base.
"""
@api_view(['GET'])
def tradieList(request):
    try:
        tradie = Tradie.objects.all()
        serializer = TradieSerializer(tradie, many=True)
        return Response(serializer.data)
    except:
        return Response({"message": "Tradies Not availble"}, status=status.HTTP_404_NOT_FOUND)


"""
This Function going to display Detailed view of one perticuler Tradie with the help of pk.
"""
@api_view(['GET'])
def tradieDetail(request, pk):
    try:
        tradie = Tradie.objects.get(id=pk)
        serializer = TradieSerializer(tradie, many=False)
        return Response(serializer.data)
    except:
        return Response({"message": "Tradies Not availble"}, status=status.HTTP_404_NOT_FOUND)


"""
This Function going to update Detailed view of one perticuler Tradie with the help of pk.
"""
@api_view(['POST'])
def tradieUpdate(request, pk):
    try:
        tradie = Tradie.objects.get(id=pk)
        serializer = TradieUpdateSerializer(instance=tradie, data=request.data)
        if serializer.is_valid():
            if request.data.get('status') == None:
                return Response({'status': ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Tradies Not availble"}, status=status.HTTP_404_NOT_FOUND)


"""
This Function going to Create A new Tradie.
"""
@api_view(['POST'])
def tradieCreate(request):
    serializer = TradieCreatreSerializer(data=request.data)
    if serializer.is_valid():
        if request.data.get('status') == None:
            return Response({'status': ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('status') == "true":
            statusTradie = True
        else:
            statusTradie = False
        Tradie.objects.create(name=request.data.get('name'), email=request.data.get('email'), contact_details=request.data.get(
            'contact_details'), phone=request.data.get('phone'), active_plans=request.data.get('active_plans'), status=statusTradie, user=request.user)
        return Response({"message": "Successfully create new tradie", "status": "true"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




"""
This Function going to Delete  view of one perticuler Tradie with the help of pk.
"""
@api_view(['DELETE'])
def tradieDelete(request, pk):
    try:
        tradie = Tradie.objects.get(id=pk)
        tradie.delete()
        return Response({"message": "Tradie deleted successfully."}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "This Tradie is no more", "status": "false"}, status=status.HTTP_404_NOT_FOUND)



"""
This Function going to update Status view of one perticuler Tradie with the help of pk.
"""
@api_view(['POST'])
def tradieStatusUpdate(request, pk):
    try:
        tradie = Tradie.objects.get(id=pk)
        if request.data.get('status') == None:
            return Response({'status': ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('status') == "true":
            statusTradie = True
        else:
            statusTradie = False
        Tradie.objects.filter(pk=tradie.pk).update(status=statusTradie)
        return Response({"message": "Tradie Status Update successfully."}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "This Tradie is no more", "status": "false"}, status=status.HTTP_404_NOT_FOUND)
