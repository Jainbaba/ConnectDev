from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializer import Room_Serializer


@api_view(['GET'])
def get_Rooms(request):
    rooms =  Room.objects.all()
    serializer = Room_Serializer(rooms,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_Room(request,index):
    room =  Room.objects.get(id=index)
    serializer = Room_Serializer(room,many=False)
    return Response(serializer.data)