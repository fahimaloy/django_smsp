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
