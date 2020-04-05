from rest_framework import serializers

from devices.models import devices, Datas


# SHOW DEVICE

class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = devices
        fields = ['title','date_published','image','category', 'id','slug']


# SHOW DATA

class DatasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Datas
        fields = ['device_id','lat', 'lng','x_acc','y_acc','z_acc','date_updated']


# Afficher USER
class DevicesSerializerUser(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = devices
        fields = ['title','date_published','image',
                  'category','username','author','slug',]

    def get_username_from_author(self,device):
        username = device.author.username
        return username



# ------ for test 1



class DevicetestSerializer(serializers.ModelSerializer):
    device_data = DatasSerializer(many=True)
    class Meta:
        model = devices
        fields = ['title', 'date_published','image','device_data','id']




class Device_Data_Serializer(serializers.ModelSerializer):
    album_musician = DatasSerializer(read_only=True, many=True)

    class Meta:
        model = devices
        fields = ['title','date_published','album_musician']

    def create(self, validated_data):
        albums_data = validated_data.pop('album_musician')
        musician = devices.objects.create(**validated_data)
        for album_data in albums_data:
            Datas.objects.create(artist=musician, **album_data)
        return musician


#for count
class CountDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = devices
        fields = ['id']