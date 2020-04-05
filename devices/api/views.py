from builtins import print
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from devices.models import devices, Datas



from devices.api.serializers import DevicesSerializer
from devices.api.serializers import DevicesSerializerUser
from devices.api.serializers import DevicetestSerializer
from devices.api.serializers import CountDevicesSerializer


#Test musicien et album

from devices.api.serializers import Device_Data_Serializer,DatasSerializer


import pickle

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


# GET ALL
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_view(request):
    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        #serializer = DevicesSerializerUser(device, many=True)
        serializer = DevicesSerializer(device, many=True)
        return Response(serializer.data)
    print(device.author)


# GET ALL by ID
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_par_id_view(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        print("All devices are : " , device)
        print("************")
        device3 = devices.objects.filter(author=user.id)
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)



# GET PAR ID / Slug
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_device_view(request, slug):
    try:
        device = devices.objects.get(slug=slug)
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if device.author != user:
        return Response({'response': "You don't have permission to See that data."})
    if request.method == 'GET':
        #serializer = DevicesSerializerUser(device)
        serializer = DevicetestSerializer(device)
        return Response(serializer.data)





@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_device_view(request, slug):
    try:
        device = devices.objects.get(slug=slug)
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if device.author != user:
        return Response({'response': "You don't have permission to edit that."})

    if request.method == 'PUT':
        serializer = DevicesSerializer(device, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = UPDATE_SUCCESS
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_device_view(request, slug):
    try:
        device = devices.objects.get(slug=slug)
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if device.author != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == 'DELETE':
        operation = device.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_device_view(request):
    device = devices(author=request.user)

    if request.method == 'POST':
        serializer = DevicesSerializer(device, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#--------------------------------------------                      Data                                       -------------------------------------------------------------


class DataListView(generics.ListCreateAPIView):
    queryset = Datas.objects.all()
    serializer_class = DatasSerializer


class DataView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DatasSerializer
    queryset = Datas.objects.all()






# GET ALL by ID
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_data_by_device_view(request, slug):

    try:
        device = devices.objects.get(slug=slug)
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if device.author != user:
        return Response({'response': "You don't have permission to see that data."})
    if request.method == 'GET':

        data1 = Datas.objects.filter(device_id=device)
        serializer = DatasSerializer(data1, many=True)
        return Response(serializer.data)





#----------------------------------------------- FILTER ---------------------------------------


# GET ALL by USER -> Category  ******* humains ************
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_par_id_humains(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        device3 = devices.objects.filter(author=user.id).filter(category="humains")
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)



# GET ALL by USER -> Category ******* animals ************
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_par_id_animals(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        device3 = devices.objects.filter(author=user.id).filter(category="animals")
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)




# GET ALL by USER -> Category ******* object ************
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_par_id_object(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        device3 = devices.objects.filter(author=user.id).filter(category="object")
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)


# GET ALL by USER -> Category ******* car ************
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_par_id_car(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        device3 = devices.objects.filter(author=user.id).filter(category="car")
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)








# COUNT ALL by USER -> Category ******************

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_count_devices_par_id(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user

        device_humains = devices.objects.filter(author=user.id).filter(category="humains").count()
        device_animals = devices.objects.filter(author=user.id).filter(category="animals").count()
        device_cars = devices.objects.filter(author=user.id).filter(category="cars").count()
        device_objects = devices.objects.filter(author=user.id).filter(category="objects").count()

        print("All devices device_humains  are : ", device_humains)
        print("All devices device_animals  are : ", device_animals)
        print("All devices device_cars  are : ", device_cars)
        print("All devices device_objects  are : ", device_objects)

        listDevices = ["All devices device_humains  are : ",device_humains,
                       "All devices device_animals  are : ",device_animals,
                       "All devices device_cars  are : ",device_cars,
                       "All devices device_objects  are : ",device_objects
                       ]

        print(listDevices)

        #serializer = CountDevicesSerializer(device3)
        return Response(listDevices)



#----------------------------------------------- ODER BY  ---------------------------------------



# GET ALL
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_date(request):
    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        device3 = devices.objects.order_by('date_published')
        #Reserved.objects.filter(client=client_id).order_by('date_published').reverse()
        print(device3)

        serializer = DevicesSerializer(device3, many=True)
        return Response(serializer.data)





@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_date_asc(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        print("All devices are : " , device)
        print("************")
        device3 = devices.objects.filter(author=user.id).order_by('date_published')
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_All_devices_date_desc(request):

    try:
        device = devices.objects.all()
    except devices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user = request.user
        print("All devices are : " , device)
        print("************")
        device3 = devices.objects.filter(author=user.id).order_by('date_published').reverse()
        print("All devices by id  are : ", device3)
        serializer = DevicesSerializerUser(device3, many=True)
        return Response(serializer.data)

