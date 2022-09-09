from dataclasses import fields
from rest_framework import serializers
from .models import *

class StudentProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['profile_pic']

class TeacherProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = ['profile_pic']

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__' 
class BatchSerializer(serializers.ModelSerializer):
    class_id = ClassesSerializer()
    class Meta:
        model = SectionOrBatch
        fields = "__all__"

class OnlineClassSerializer(serializers.ModelSerializer):
    batch_id = BatchSerializer()
    class Meta:
        model = OnlineClass
        fields = ['id','online_class_name','online_class_link','batch_id','status']
