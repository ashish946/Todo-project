from rest_framework import serializers
from todowo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created=serializers.ReadOnlyField()
    datecompleted=serializers.ReadOnlyField()
    class Meta:
        model=Todo
        fields=['id','title','memo','created','datecompleted','important']


class TodoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=['id']
        read_only_fields=['title','memo','created','datecompleted','important']
