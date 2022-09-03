from rest_framework import serializers
from mycode.models import MyCode

class MyCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyCode
        fields = ['id','code_name','code','language']

