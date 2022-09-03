# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver





# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Teacher"), (3, "Student"),(4,"Accountant"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)



class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Teachers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    presentAddress = models.TextField(null=True)
    parmanentAddress = models.TextField(null=True)
    mobileNumber = models.CharField(max_length=14,null=True)
    emergencyMobileNumber = models.CharField(max_length=14,null=True)
    sscBoard = models.CharField(max_length=30,null=True)
    sscPassingYear = models.IntegerField(null=True)
    sscGPA = models.FloatField(null=True)
    sscGroup = models.TextField(max_length=30,null=True)
    hscBoard = models.CharField(max_length=30,null=True)
    hscPassingYear = models.IntegerField(null=True)
    hscGPA = models.FloatField(null=True)
    hscGroup = models.TextField(max_length=30,null=True)
    baUniversity = models.CharField(max_length=30,null=True)
    nid = models.CharField(max_length=50,null=True)
    mstatus = models.CharField(max_length=50,null=True)
    baPassingYear = models.IntegerField(null=True)
    baCGPA = models.FloatField(null=True)
    baSubject = models.TextField(max_length=30,null=True)
    gender = models.IntegerField(null=True)
    currentInstitute = models.CharField(max_length=500,null=True)
    dateOfBirth = models.DateField(null=True)
    experience = models.TextField(null=True)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_pic = models.FileField(null=True)
    
    objects = models.Manager()
    
    def __str__(self):
	    return self.admin.first_name + " "  +  self.admin.last_name 

class Accountants(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    presentAddress = models.TextField(null=True)
    parmanentAddress = models.TextField(null=True)
    mobileNumber = models.CharField(max_length=14,null=True)
    emergencyMobileNumber = models.CharField(max_length=14,null=True)
    gender = models.IntegerField(null=True)
    dateOfBirth = models.DateField(null=True)
    experience = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
	    return self.admin.first_name + " "  +  self.admin.last_name 

class Classes(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):
	#     return self.id

class SectionOrBatch(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes,on_delete=models.CASCADE,default=1)
    batch_name = models.CharField(max_length=100)
    objects = models.Manager()



class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default=1) #need to give defauult course
    batch_id = models.ForeignKey(SectionOrBatch, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    def __str__(self):
	    return self.subject_name

class Payment_Teacher(models.Model) :
    id = models.AutoField(primary_key=True)
    paying_date = models.DateTimeField(auto_now_add=True) 
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_upto = models.DateTimeField(auto_now=False,auto_now_add=False)
    objects = models.Manager()





class PCC(models.Model) :
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE) 
    batch_id = models.ForeignKey(SectionOrBatch, on_delete=models.CASCADE) 
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    objects = models.Manager()
    def __str__(self):
	    
        return  self.class_id.class_name +" " +self.subject_id.subject_name +" " 




class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    smsMobile  = models.CharField(max_length=14,null=True)
    class_id = models.ForeignKey(Classes, on_delete=models.DO_NOTHING,null=True)
    batch_id = models.ForeignKey(SectionOrBatch, on_delete=models.CASCADE,null=True)
    fathersName = models.CharField(max_length=100,null=True)
    fathersProfession = models.CharField(max_length=100 , null=True)
    fathersMobile  = models.CharField(max_length=14,null=True)
    mothersName = models.CharField(max_length=100,null=True)
    mothersProfession = models.CharField(max_length=100 , null=True)
    mothersMobile  = models.CharField(max_length=14,null=True)
    dateOfBirth = models.DateField(auto_now=False,auto_now_add=False,null=True)
    school = models.CharField(max_length=500,null=True)
    presentAddress = models.TextField(max_length=5000 , null=True)
    parmanentAddress = models.TextField(max_length=5000,null=True)
    mobile = models.CharField(max_length=14,null=True)    
    feesAmount = models.IntegerField(default=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active_status = models.BooleanField(default=True)
    objects = models.Manager()


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes,on_delete=models.CASCADE,null=True)
    attendance_date = models.DateField()
    batch_id = models.ForeignKey(SectionOrBatch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
############





class FeesReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classes, on_delete=models.DO_NOTHING,default=1)
    batch_id = models.ForeignKey(SectionOrBatch, on_delete=models.CASCADE,default=1)
    fees_title = models.CharField(max_length=25)
    extra_fees_title = models.CharField(max_length=25,null=True)
    fees_date = models.DateTimeField()
    status = models.BooleanField(default=False)
    paid_status = models.IntegerField(default=0)
    action = models.IntegerField(default=0)    
    paid_at = models.DateTimeField(null=True)
    bkash_nmb = models.CharField(max_length=13,null=True)
    trans_id = models.CharField(max_length=100,null=True)
    in_cash = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    extra_amount = models.IntegerField(default=0)
    objects = models.Manager()




############

class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

##################
##################
class PDFDetails(models.Model):
    img = models.FileField()

class PaymentStudent(models.Model):
    id = models.AutoField(primary_key=True)
    fees_id = models.ForeignKey(FeesReport,on_delete=models.CASCADE,default = 3)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    pay_upto = models.CharField(max_length=255)
    bkash_nmb = models.CharField(max_length=13)
    amount = models.IntegerField()
    trans_id = models.CharField(max_length=100)
    payment_status = models.IntegerField(default=0)
    in_cash = models.IntegerField(default=0)
    class_id = models.ForeignKey(Classes,default=1,on_delete=models.CASCADE)
    batch_id = models.ForeignKey(SectionOrBatch,default=1,on_delete=models.CASCADE)
    paid_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class ClassAndPayment(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    pcc_id = models.ForeignKey(PCC, on_delete=models.CASCADE, default=1)
    class_date = models.CharField(max_length=255)
    per_class_charge = models.CharField(max_length=255)
    from_time = models.CharField(max_length=100)
    to_time = models.CharField(max_length=100 , default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
	    
        return  self.teacher_id.admin.first_name +" "+ self.teacher_id.admin.last_name+"-" +self.class_date+"-" + self.pcc_id.class_id.class_name

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackTeachers(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Notices(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(SectionOrBatch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
# class NotificationStudent(models.Model):
#     id = models.AutoField(primary_key=True)
#     student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = models.Manager()


# class NotificationTeachers(models.Model):
#     id = models.AutoField(primary_key=True)
#     stafff_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = models.Manager()

class CustomSMS(models.Model):
    number = models.TextField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    

class OnlineClass(models.Model):
    id = models.AutoField(primary_key=True)
    online_class_name = models.CharField(max_length=100)
    online_class_link = models.CharField(max_length=500)
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(SectionOrBatch,on_delete=models.CASCADE)
    
class Examination(models.Model):
    id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100)
    exam_date = models.DateField(auto_now=False, auto_now_add=False)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(SectionOrBatch,on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

class TotalMarks(models.Model):
    id=models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Examination,on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    obtained_marks = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    exam_date = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
	    
        return  self.exam_id.exam_name + " " + self.student_id.admin.first_name
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True,max_length=255)
    phone = models.CharField(null=True,max_length=255)
    message = models.TextField()
    
class AdditionalExpenses(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=5000)
    date = models.DateField()
    amount = models.IntegerField()
    objects = models.Manager()

class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    exam_id = models.ForeignKey(Examination, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)    
    # class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.IntegerField(default=0)
    subject_assignment_marks = models.IntegerField(default=0)
    gpa = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=350)
    desc = models.TextField()
    attachment = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Notifications(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=555)
    status = models.BooleanField(default=False)
    link = models.CharField(max_length=555,default="")
    created_at = models.DateTimeField(auto_now_add=True)    

#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in Admin, Teacher or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Teachers.objects.create(admin=instance,profile_pic="",)
        if instance.user_type == 3:
            Students.objects.create(admin=instance, profile_pic="", gender="")
        if instance.user_type == 4:
            Accountants.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.teachers.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.accountants.save()
    


