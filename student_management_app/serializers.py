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
class SubjectSerializer(serializers.ModelSerializer):
    batch_id = BatchSerializer()
    class Meta:
        model = Subjects
        fields = "__all__"

class OnlineClassSerializer(serializers.ModelSerializer):
    batch_id = BatchSerializer()
    class Meta:
        model = OnlineClass
        fields = ['id','online_class_name','online_class_link','batch_id','status']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__'
        exclude = ('password',)
        
class TeacherSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    class Meta:
        model = Teachers
        fields = "__all__"
class StudentSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    class Meta:
        model = Students
        fields = "__all__"
       
class TeacherPaymentSerializer(serializers.ModelSerializer):
    teacher_id = TeacherSerializer()
    class Meta:
        model = Payment_Teacher
        fields = "__all__"
class PCCSerializer(serializers.ModelSerializer):
    teacher_id = TeacherSerializer()
    batch_id = BatchSerializer()
    subject_id = SubjectSerializer()
    class Meta:
        model = PCC
        fields = "__all__"
class RegisteredClassSerializer(serializers.ModelSerializer):
    teacher_id = TeacherSerializer()
    pcc_id = PCCSerializer()
    class Meta:
        model = ClassAndPayment
        fields = "__all__"
class StudentPaymentSerializer(serializers.ModelSerializer):
    student_id = StudentSerializer()
    batch_id = BatchSerializer()
    class Meta:
        model = FeesReport
        fields = "__all__"
        
class AdditionalExpensesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdditionalExpenses
        fields = "__all__"
        
