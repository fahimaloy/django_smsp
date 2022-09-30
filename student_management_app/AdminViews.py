import io
import re
from tokenize import Number
from django.contrib.messages.api import error
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context, context
import requests
import datetime
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime
from student_management_app.models import Accountants, Notifications, PDFDetails ,CustomUser,AdditionalExpenses , CustomSMS , OnlineClass , Notices, PDFDetails , Teachers, TotalMarks , Examination , StudentResult , Classes, Subjects, Students, SectionOrBatch, FeedBackStudent, FeedBackTeachers, LeaveReportStudent,  ClassAndPayment, Attendance, AttendanceReport, PaymentStudent ,Payment_Teacher , FeesReport ,PCC
from student_management_app.serializers import *




def admin_home(request):
    totalUnpaidAmount = list(ClassAndPayment.objects.filter(status=1).aggregate(Sum('per_class_charge')).values())[0] or 0
    totalPaidAmount = list(Payment_Teacher.objects.all().order_by('-payment_upto').aggregate(Sum('payment_amount')).values())[0] or 0
    totalRemainingAdditionalAmount = list(FeesReport.objects.filter(paid_status = 0).aggregate(Sum('extra_amount')).values())[0] or 0
    totalRemainingAmount = list(FeesReport.objects.filter(paid_status = 0).aggregate(Sum('amount')).values())[0] or 0
    ObtainedAmount = list(FeesReport.objects.filter(paid_status=1).order_by("-paid_at").aggregate(Sum('amount')).values())[0] or 0
    AdditionalObtainedAmount = list(FeesReport.objects.filter(paid_status=1).order_by("-paid_at").aggregate(Sum('extra_amount')).values())[0] or 0
    totalObtainedAmount = ObtainedAmount + AdditionalObtainedAmount
    AdditionalExpenseAmount = list(AdditionalExpenses.objects.all().order_by("-date").aggregate(Sum('amount')).values())[0] or 0
    totalAdditionalExpenseAmount = totalPaidAmount + AdditionalExpenseAmount or 0
    totalDueAmount = totalUnpaidAmount - totalPaidAmount
    totalProfit = totalObtainedAmount - totalAdditionalExpenseAmount
    
    all_student_count = Students.objects.filter(active_status=True).count()
    subject_count = SectionOrBatch.objects.all().count()
    class_count = Classes.objects.all().count()
    teacher_count = Teachers.objects.filter(active_status=True).count()
    # Total Subjects and students in Each class
    class_all = Classes.objects.all()
    class_name_list = []
    subject_count_list = []
    student_count_list_in_class = []

    for classes in class_all:
        # subjects = Subjects.objects.filter(class_id=classes.id).count()
        subjects = 0
        students = Students.objects.filter(class_id=classes.id).count()
        class_name_list.append(classes.class_name)
        subject_count_list.append(subjects)
        student_count_list_in_class.append(students)
    
    # For Saffs
    teacher_attendance_present_list=[]
    teacher_registered_class_list=[]
    teacher_name_list=[]

    teachers = Teachers.objects.filter(active_status=True)
    for teacher in teachers:
        # subject_ids = Subjects.objects.filter(teacher_id=teacher.admin.id)
        # attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        reg = ClassAndPayment.objects.filter(teacher_id=teacher.id, status=1).count()
        # teacher_attendance_present_list.append(attendance)
        teacher_registered_class_list.append(reg)
        teacher_name_list.append(teacher.admin.first_name)

    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)
    reg_classes = ClassAndPayment.objects.filter(status=0).count()
    st_p_req = FeesReport.objects.filter(status=0).count()


    context={
        "paidAmount": totalPaidAmount,
        "unpaidAmunt" : totalUnpaidAmount,
        "dueAmount" : totalDueAmount,
        "profitAmount" : totalProfit,
        "obtainedAmount": totalObtainedAmount,
        "remainingAmount":totalRemainingAmount,
        "st_p_req" : st_p_req ,
        "reg_classes" : reg_classes ,
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "class_count": class_count,
        "teacher_count": teacher_count,
        "class_name_list": class_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_class": student_count_list_in_class,
        "teacher_attendance_present_list": teacher_attendance_present_list,
        "teacher_registered_class_list": teacher_registered_class_list,
        "teacher_name_list": teacher_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    return render(request, "admin_template/home_content.html", context)


def add_teacher(request):
    return render(request, "admin_template/add_teacher_template.html")


def add_teacher_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_teacher')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        nid = request.POST.get('nid')
        email = request.POST.get('email')
        password = request.POST.get('password')
        presentAddress = request.POST.get('presentAddress')
        parmanentAddress = request.POST.get('parmanentAddress')
        mobileNumber = request.POST.get('mobileNumber')
        emergencyMobileNumber = request.POST.get('emergencyMobileNumber')
        gender = request.POST.get('gender')
        sscBoard = request.POST.get('sscBoard')
        sscGroup = request.POST.get('sscGroup')
        sscPassingYear = request.POST.get('sscPassingYear')
        sscGPA = request.POST.get('sscGPA')
        hscBoard = request.POST.get('hscBoard')
        hscGroup = request.POST.get('hscGroup')
        hscPassingYear = request.POST.get('hscPassingYear')
        hscGPA = request.POST.get('hscGPA')
        baUniversity = request.POST.get('baUniversity')
        baSubject = request.POST.get('baSubject')
        baPassingYear = request.POST.get('baPassingYear')
        baCGPA = request.POST.get('baCGPA')
        dateOfBirth = request.POST.get('dateOfBirth')
        experience = request.POST.get('experience')
        currentInstitute = request.POST.get('currentInstitute')
        mstatus = request.POST.get('mstatus')
        payment_type = request.POST.get('payment_type')
        monthly_payment = request.POST.get('monthly_payment') or 0
        
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.teachers.presentAddress = presentAddress
            user.teachers.parmanentAddress = parmanentAddress
            user.teachers.mobileNumber = mobileNumber
            user.teachers.emergencyMobileNumber = emergencyMobileNumber
            user.teachers.gender = gender
            user.teachers.sscBoard = sscBoard
            user.teachers.sscGroup = sscGroup
            user.teachers.sscPassingYear = sscPassingYear
            user.teachers.sscGPA = sscGPA
            user.teachers.hscBoard = hscBoard
            user.teachers.hscGroup = hscGroup
            user.teachers.hscPassingYear = hscPassingYear
            user.teachers.hscGPA = hscGPA
            user.teachers.baSubject = baSubject
            user.teachers.nid = nid
            user.teachers.baUniversity = baUniversity
            user.teachers.baPassingYear = baPassingYear
            user.teachers.baCGPA = baCGPA
            user.teachers.dateOfBirth = dateOfBirth
            user.teachers.experience = experience
            user.teachers.currentInstitute = currentInstitute
            user.teachers.mstatus = mstatus
            user.teachers.profile_pic = profile_pic_url
            if payment_type == 1 or payment_type == "1":
                user.teachers.monthly_payment_type = True
                user.teachers.monthly_payment = monthly_payment
            user.save()
            phoneNumber = "88"+str(mobileNumber)
            message_body = "Welcome to Alim's Academy "+ first_name +" "+ last_name +"!! We are very Glad to have you as a valuable part of Our Institute. Your Login Details are given Below:"+ " Username : "+ str(username)+" Password :" +str(password) +" URL: https://www.alimsacademy.xyz . Best Regards. Alim's Academy!"
            url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

            payload  = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            #response = requests.request("POST", url, headers=headers, data = payload)

            
            messages.success(request, "teacher Added Successfully!")
            return redirect('add_teacher')
        except:
            messages.error(request, "Failed to Add teacher!")
            return redirect('add_teacher')



def manage_teacher(request):
    teachers = Teachers.objects.all()
    context = {
        "teachers": teachers
    }
    return render(request, "admin_template/manage_teacher_template.html", context)


def edit_teacher(request, teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
    date = teacher.dateOfBirth
    birthDate = datetime.strftime(date , "%Y-%m-%d")

    context = {
        "birthDate" : birthDate ,
        "teacher": teacher,
        "id": teacher_id
    }
    return render(request, "admin_template/edit_teacher_template.html", context)


def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id = request.POST.get('teacher_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        presentAddress = request.POST.get('presentAddress')
        parmanentAddress = request.POST.get('parmanentAddress')
        mobileNumber = request.POST.get('mobileNumber')
        emergencyMobileNumber = request.POST.get('emergencyMobileNumber')
        gender = request.POST.get('gender')
        sscBoard = request.POST.get('sscBoard')
        sscGroup = request.POST.get('sscGroup')
        sscPassingYear = request.POST.get('sscPassingYear')
        sscGPA = request.POST.get('sscGPA')
        hscBoard = request.POST.get('hscBoard')
        hscGroup = request.POST.get('hscGroup')
        hscPassingYear = request.POST.get('hscPassingYear')
        hscGPA = request.POST.get('hscGPA')
        baUniversity = request.POST.get('baUniversity')
        baSubject = request.POST.get('baSubject')
        baPassingYear = request.POST.get('baPassingYear')
        baCGPA = request.POST.get('baCGPA')
        dateOfBirth = request.POST.get('dateOfBirth')
        experience = request.POST.get('experience')
        currentInstitute = request.POST.get('currentInstitute')
        nid = request.POST.get('nid')
        mstatus = request.POST.get('mstatus')
        payment_type = request.POST.get('payment_type')
        monthly_payment = request.POST.get('monthly_payment') or 0
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        

            
        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            if password != None and password != "":
                user.set_password(password)
                teacher = Teachers.objects.get(admin=user.id)
                phoneNumber = "88"+teacher.mobileNumber
                message_body = "Congratulations!Your Password Have been Changed by the Authourity. Your New Login Details are given below : Username: "+ user.username +" Password: "+ password+" . Best Regards Alim's Academy"
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }

                #response = requests.request("POST", url, headers=headers, data = payload)

            user.save()
            
            # INSERTING into teacher Model
            teacher_model = Teachers.objects.get(admin=teacher_id)
            
            teacher_model.presentAddress = presentAddress
            teacher_model.nid = nid
            teacher_model.parmanentAddress = parmanentAddress
            teacher_model.mobileNumber = mobileNumber
            teacher_model.emergencyMobileNumber = emergencyMobileNumber
            teacher_model.gender = gender
            teacher_model.sscBoard = sscBoard
            teacher_model.sscGroup = sscGroup
            teacher_model.sscPassingYear = sscPassingYear
            teacher_model.sscGPA = sscGPA
            teacher_model.hscBoard = hscBoard
            teacher_model.hscGroup = hscGroup
            teacher_model.hscPassingYear = hscPassingYear
            teacher_model.hscGPA = hscGPA
            teacher_model.baSubject = baSubject
            teacher_model.baUniversity = baUniversity
            teacher_model.baPassingYear = baPassingYear
            teacher_model.baCGPA = baCGPA
            teacher_model.dateOfBirth = dateOfBirth
            teacher_model.experience = experience
            teacher_model.currentInstitute = currentInstitute
            teacher_model.mstatus = mstatus
            if profile_pic_url != None:
                teacher_model,profile_pic = profile_pic_url
            if payment_type == 1 or payment_type == "1":
                teacher_model.monthly_payment_type = True
                teacher_model.monthly_payment = monthly_payment
            elif payment_type == 0 or payment_type == "0":
                teacher_model.monthly_payment_type = False
                teacher_model.monthly_payment = 0
            teacher_model.save()

            messages.success(request, "teacher Updated Successfully.")
            return redirect('/edit_teacher/'+teacher_id)

        except:
            messages.error(request, "Failed to Update teacher.")
            return redirect('/edit_teacher/'+teacher_id)



def delete_teacher(request, teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
    user = CustomUser.objects.get(id=teacher_id)
    try:
        teacher.delete()
        user.delete()
        messages.success(request, "teacher Deleted Successfully.")
        return redirect('manage_teacher')
    except:
        messages.error(request, "Failed to Delete teacher.")
        return redirect('manage_teacher')




def add_class(request):
    return render(request, "admin_template/add_class_template.html")


def add_class_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_class')
    else:
        classes = request.POST.get('class')
        try:
            class_model = Classes(class_name=classes)
            class_model.save()
            messages.success(request, "Class Added Successfully!")
            return redirect('add_class')
        except:
            messages.error(request, "Failed to Add Class!")
            return redirect('add_class')


def manage_class(request):
    classes = Classes.objects.all()
    context = {
        "classes": classes
    }
    return render(request, 'admin_template/manage_class_template.html', context)


def edit_class(request, class_id):
    classes = Classes.objects.get(id=class_id)
    context = {
        "class": classes,
        "id": class_id
    }
    return render(request, 'admin_template/edit_class_template.html', context)


def edit_class_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        class_id = request.POST.get('class_id')
        class_name = request.POST.get('class')

        try:
            classes = Classes.objects.get(id=class_id)
            classes.class_name = class_name
            classes.save()

            messages.success(request, "Class Updated Successfully.")
            return redirect('/edit_class/'+class_id)

        except:
            messages.error(request, "Failed to Update Class.")
            return redirect('/edit_class/'+class_id)


def delete_class(request, class_id):
    classes = Classes.objects.get(id=class_id)
    try:
        classes.delete()
        messages.success(request, "Class Deleted Successfully.")
        return redirect('manage_class')
    except:
        messages.error(request, "Failed to Delete Class.")
        return redirect('manage_class')


def manage_batch(request):
    batch = SectionOrBatch.objects.all()
    context = {
        "batchs": batch
    }
    return render(request, "admin_template/manage_batch_template.html", context)


def add_batch(request):
    classes = Classes.objects.all()
    context = {
        "classes" : classes ,
    }
    return render(request, "admin_template/add_batch_template.html" , context)


def add_batch_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_class')
    else:
        batch_name = request.POST.get('batch_name')
        class_id = request.POST.get('classes')
        

        try:
            class_obj = Classes.objects.get(id=class_id)
            batch = SectionOrBatch(batch_name=batch_name,class_id=class_obj)
            batch.save()
            messages.success(request, "batch Year added Successfully!")
            return redirect("add_batch")
        except:
            messages.error(request, "Failed to Add batch Year")
            return redirect("add_batch")


def edit_batch(request, batch_id):
    batch = SectionOrBatch.objects.get(id=batch_id)
    context = {
        "batch": batch
    }
    return render(request, "admin_template/edit_batch_template.html", context)


def edit_batch_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_batch')
    else:
        batch_id = request.POST.get('batch_id')
        batch_name = request.POST.get('batch_name')
        

        try:
            batch = SectionOrBatch.objects.get(id=batch_id)
            batch.batch_name = batch_name
            
            batch.save()

            messages.success(request, "batch Year Updated Successfully.")
            return redirect('/edit_batch/'+batch_id)
        except:
            messages.error(request, "Failed to Update batch Year.")
            return redirect('/edit_batch/'+batch_id)


def delete_batch(request, batch_id):
    batch = SectionOrBatch.objects.get(id=batch_id)
    try:
        batch.delete()
        messages.success(request, "batch Deleted Successfully.")
        return redirect('manage_batch')
    except:
        messages.error(request, "Failed to Delete batch.")
        return redirect('manage_batch')


def add_student(request):
    # form = AddStudentForm()
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()


    context = {
        # "form": form
        "classes" : classes ,
        "batches" : batches ,
    }
    return render(request, 'admin_template/add_student_template.html', context)




def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        

    
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        batch_id = request.POST.get('batch_id')
        class_id = request.POST.get('class_id')
        gender = request.POST.get('gender')
        fathersName = request.POST.get('fathersName')
        fathersProfession = request.POST.get('fathersProfession')
        fathersMobile = request.POST.get('fathersMobile')
        mothersName = request.POST.get('mothersName')
        mothersProfession = request.POST.get('mothersProfession')
        mothersMobile = request.POST.get('mothersMobile')
        presentAddress = request.POST.get('presentAddress')
        parmanentAddress = request.POST.get('parmanentAddress')
        mobile = request.POST.get('mobile')
        dateOfBirth = request.POST.get('dateOfBirth')
        school = request.POST.get('school')
        fees = request.POST.get('fees')
        smsMobile = request.POST.get('smsMobile')
        regFees = request.POST.get('regFees')



        # Getting Profile Pic first
        # First Check whether the file is selected or not
        # Upload only if file is selected
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            
    
            class_obj = Classes.objects.get(id=class_id)
            user.students.class_id = class_obj
    
            batch_obj = SectionOrBatch.objects.get(id=batch_id)
            user.students.batch_id = batch_obj
    
            user.students.gender = gender
    
    
            user.students.fathersName = fathersName
            user.students.fathersProfession = fathersProfession
            user.students.fathersMobile = fathersMobile
            user.students.mothersName = mothersName
            user.students.mothersProfession = mothersProfession
            user.students.mothersMobile = mothersMobile
            user.students.presentAddress = presentAddress
            user.students.parmanentAddress = parmanentAddress
            user.students.mobile = mobile
            user.students.dateOfBirth = dateOfBirth
            user.students.school = school
            user.students.feesAmount = fees
            user.students.smsMobile = smsMobile
            
            user.students.profile_pic = profile_pic_url
            user.save()
            students = Students.objects.get(admin=user)
            admission = FeesReport(student_id=students,class_id=class_obj,batch_id=batch_obj,fees_title="Registration Fees",fees_date=students.created_at,amount=regFees,extra_amount=0,extra_fees_title="N/A",action=3,in_cash=1)
            admission.save()
            phoneNumber = "88"+str(smsMobile)
            message_body = " অভিনন্দন"+ first_name +" "+ last_name +" আপনার / আপনার সন্তানের আলিম'স অ্যাকাডেমি তে রেজিস্ট্রেশন সম্পন্ন হয়েছে । আপনার লগইন বিশরদ নিচে দেয়া হলো "+ " CoachingID : "+ str(username)+" Password :" +str(password) +" URL: https://www.alimsacademy.com . ধন্যবাদান্তে আলিম'স একাডেমি!"
            url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""
    
            payload  = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
    
            #response = requests.request("POST", url, headers=headers, data = payload)
    
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')
   


def manage_student(request):
    students = Students.objects.all()
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    context = {
        "students": students,
        "classes" : classes ,
        "batches" : batches ,
    }
    return render(request, 'admin_template/manage_student_template.html', context)


def edit_student(request, student_id):

    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    students = Students.objects.get(admin=student_id)
    date = students.dateOfBirth
    birthDate = datetime.strftime(date , "%Y-%m-%d")


    context = {
        "birthDate" : birthDate ,
        "students": students ,
        "classes" : classes ,
        "batches" : batches ,
    }    

    return render(request, "admin_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        
        
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')        
        batch_id = request.POST.get('batch_id')
        class_id = request.POST.get('class_id')
        gender = request.POST.get('gender')
        fathersName = request.POST.get('fathersName')
        fathersProfession = request.POST.get('fathersProfession')
        fathersMobile = request.POST.get('fathersMobile')
        mothersName = request.POST.get('mothersName')
        mothersProfession = request.POST.get('mothersProfession')
        mothersMobile = request.POST.get('mothersMobile')
        presentAddress = request.POST.get('presentAddress')
        parmanentAddress = request.POST.get('parmanentAddress')
        mobile = request.POST.get('mobile')
        dateOfBirth = request.POST.get('dateOfBirth')
        school = request.POST.get('school')
        fees = request.POST.get('fees')
        smsMobile = request.POST.get('smsMobile')

        # Getting Profile Pic first
        # First Check whether the file is selected or not
        # Upload only if file is selected
        # request.FILES.get('url')
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            # First Update into Custom User Model
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            
    
            # Then Update Students Table
            student_model = Students.objects.get(admin=student_id)
            # student_model.address = address
    
            classes = Classes.objects.get(id=class_id)
            student_model.class_id = classes
    
            batch_obj = SectionOrBatch.objects.get(id=batch_id)
            student_model.batch_id = batch_obj
            student_model.gender = gender
            student_model.fathersName = fathersName
            student_model.fathersProfession = fathersProfession
            student_model.fathersMobile = fathersMobile
            student_model.mothersName = mothersName
            student_model.mothersProfession = mothersProfession
            student_model.mothersMobile = mothersMobile
            student_model.presentAddress = presentAddress
            student_model.parmanentAddress = parmanentAddress
            student_model.mobile = mobile
            student_model.dateOfBirth = dateOfBirth
            student_model.school = school
            student_model.feesAmount = fees
            student_model.smsMobile = smsMobile
    
            if profile_pic_url != None:
                student_model.profile_pic = profile_pic_url
            student_model.save()
            if password != None and password != "":
                user.set_password(password)
                student = Students.objects.get(admin=user.id)
                phoneNumber = "88"+student.smsMobile
                message_body = "Congratulations "+ user.first_name +" "+ user.last_name +"!Your Password Have been Changed by the Authourity. Your New Login Details are given below : CoachingID: "+ user.username +" Password: "+ password+" . Best Regards Alim's Academy"
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""
    
                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
                #response = requests.request("POST", url, headers=headers, data = payload)

    
                
            
            
            user.save()
            messages.success(request, "Student Updated Successfully!")
            return redirect('/edit_student/'+student_id)
        except:
            messages.error(request, "Failed to Update Student.")
            return redirect('/edit_student/'+student_id)
    


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    customUser = CustomUser.objects.get(id=student.admin.id)
    try:
        customUser.delete()
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    classes = Classes.objects.all()
    
    context = {
        "classes": classes,
        
    }
    return render(request, 'admin_template/add_subject_template.html', context)



def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        try:
            subject_name = request.POST.get('subject')
            class_id = request.POST.get('classes')
            batch_id = request.POST.get('batch')
            classes = Classes.objects.get(id=class_id)
            batch_obj = SectionOrBatch.objects.get(id=batch_id)
            
            subject = Subjects(subject_name=subject_name, class_id=classes , batch_id=batch_obj)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'admin_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    classes = Classes.objects.all()
    
    context = {
        "subject": subject,
        "classes": classes,
        
    
    }
    return render(request, 'admin_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        class_id = request.POST.get('classes')
        batch_id = request.POST.get('batch')
    

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            classes = Classes.objects.get(id=class_id)
            batch_obj = SectionOrBatch.objects.get(id=batch_id)
            subject.class_id = classes
            subject.batch_id = batch_obj
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            # return redirect('/edit_subject/'+subject_id)



def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_roll_exist(request):
    roll = request.POST.get("roll")
    class_id = request.POST.get("class_id")
    class_obj = Classes.objects.get(id=class_id)
    user_obj = Students.objects.filter(roll=roll , class_id=class_obj).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def single_student_feedback(request,feedback_id):
    feedback = FeedBackStudent.objects.get(id=feedback_id)
    context={
        "feedback":feedback
    }
    return render(request,"admin_template/single_student_feedback.html",context)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")
def single_teacher_feedback(request,feedback_id):
    feedback = FeedBackTeachers.objects.get(id=feedback_id)
    context={
        "feedback":feedback
    }
    return render(request,"admin_template/single_teacher_feedback.html",context)


def teacher_feedback_message(request):
    feedbacks = FeedBackTeachers.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_template/teacher_feedback_template.html', context)


@csrf_exempt
def teacher_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackTeachers.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")

def single_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    context={
        "leave":leave
    }
    return render(request,"admin_template/single_leave.html",context)

def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'admin_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def student_payment_view(request):
    payments = FeesReport.objects.all().order_by('-paid_at')
    

    context = {
        "payments": payments
    }
    return render(request, 'admin_template/view_student_payment.html', context)

def student_payment_approve(request, payment_id):
    payment = FeesReport.objects.get(id=payment_id)
    payment.paid_status = 1
    payment.action = 1
    payment.paid_at = datetime.now()

    phoneNumber = "88"+str(payment.student_id.smsMobile)
    # message_body = "অভিনন্দন!"+str(payment.student_id.admin.first_name)+" "+str(payment.student_id.admin.last_name)+"এর "+ str(payment.fees_title) +"বাবদ "+str(payment.amount)+"টাকা পরিশোধিত হয়েছে । ধন্যবাদান্তে আলিম'স অ্যাকাডেমি ।    "
    message_body = "অভিনন্দন! নামঃ "+str(payment.student_id.admin.first_name)+" "+str(payment.student_id.admin.last_name)+"("+str(payment.student_id.admin.username)+ ") শ্রেনিঃ "+str(payment.student_id.class_id.class_name)+"("+ str(payment.student_id.batch_id.batch_name) +") "+ str(payment.fees_title) +" বাবদ "+str(payment.amount)+"টাকা পরিশোধ করা হয়েছে । ধন্যবাদান্তে আলিম'স অ্যাকাডেমি " 
    url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

    payload  = {}
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    #response = requests.request("POST", url, headers=headers, data = payload)

    # print(response.text.encode('utf8'))
    # print(url)
    
    payment.save()
    return redirect('student_payment_view')


def student_payment_reject(request, payment_id):
    payment = FeesReport.objects.get(id=payment_id)
    payment.action = 2
    payment.save()
    return redirect('student_payment_view')


def TeacherPayment(request):
    teacher = Teachers.objects.all()

    context = {
        "teacher" : teacher,
        
    }
    return render(request, 'admin_template/teacher_payment.html', context)


def TeacherPaymentSingle(request, teacher_id):

    try:
        payment_details = Payment_Teacher.objects.filter(teacher_id=teacher_id).order_by('-payment_upto')
        teacher_obj = Teachers.objects.get(id=teacher_id)
        # leave_data = ClassAndPayment.objects.filter(teacher_id=teacher_obj)
        approved_class = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)

            
        ll = approved_class.aggregate(Sum('per_class_charge'))

        al = list(ll.values())[0]
        
        payment_data = Payment_Teacher.objects.filter(teacher_id=teacher_obj).order_by('-payment_upto')
        
        total_payment_dict = payment_data.aggregate(Sum('payment_amount'))
        total_payment_list_value = list(total_payment_dict.values())[0]

        due_payment = al - total_payment_list_value

        CaP = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)
        
        si = teacher_id


        context = {
            "si" : si ,
            "teacher_obj" : teacher_obj ,
            "CaP" : CaP ,
            "total_payment_list_value" : total_payment_list_value ,
            "al" : al ,
            "due_payment" : due_payment ,
            "payment_details" : payment_details ,
            
        }
        return render(request, 'admin_template/teacher_payment_single.html', context)

    except:
        
        CaP = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)
        payment_details = Payment_Teacher.objects.filter(teacher_id=teacher_id).order_by('-payment_upto')
        teacher_obj = Teachers.objects.get(id=teacher_id)
        si = teacher_id
        context = {
            "CaP" : CaP ,
            "si" : si ,

            "payment_details" : payment_details ,
            
        }
        return render(request, 'admin_template/teacher_payment_single.html', context)

@csrf_exempt
def add_teachers_payment(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect(reverse('teacher_payment_date_filter'))
    else:
        try:
            teacher_id = request.POST.get('teachers')
            pay_upto  = request.POST.get('paymentUpto')
            payment_amount = request.POST.get('paymentAmount')
            payment_id = request.POST.get('payment_id')

            teacher_obj = Teachers.objects.get(id=teacher_id)
            if(teacher_obj.monthly_payment_type and payment_id != 0):
                payment = Payment_Teacher.objects.get(id=payment_id)
                payment.paid = True

            else:
                payment = Payment_Teacher(teacher_id=teacher_obj,payment_upto=pay_upto, payment_amount=payment_amount,paid=True)
                phoneNumber = "88"+str(teacher_obj.mobileNumber)
                message_body = "Dear "+teacher_obj.admin.first_name+" "+teacher_obj.admin.last_name+" Sir,  "+payment_amount +" ৳ honorium has been paid as your contribution to the institute upto "+str(pay_upto)+" . We appreciate your cooperation. Best Regards! Alim's Academy"
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }

                #response = requests.request("POST", url, headers=headers, data = payload)

            payment.save()
            return HttpResponse("True")

        except:
            return HttpResponse("False")




def teacher_class_reg(request):
    regs = ClassAndPayment.objects.all().order_by("-class_date")
    

    context = {
        
        "regs": regs ,
    }
    return render(request, 'admin_template/teacher_class_reg.html', context)


def teacher_class_reg_approve(request, reg_id):
    leave = ClassAndPayment.objects.get(id=reg_id)
    leave.status = 1
    leave.save()
    return redirect('teacher_class_reg')


def teacher_class_reg_reject(request, reg_id):
    leave = ClassAndPayment.objects.get(id=reg_id)
    leave.status = 2
    leave.save()
    return redirect('teacher_class_reg')


def admin_view_attendance(request):
    classes = Classes.objects.all()
    # batch = SectionOrBatch.objects.all()
    context = {
        "classes": classes,
        # "batches": batch
    }
    return render(request, "admin_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    class_id = request.POST.get("class_id")
    batch = request.POST.get("batch_id")

    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    class_model = Classes.objects.get(id=class_id)

    batch_model = SectionOrBatch.objects.get(id=batch)

    # students = Students.objects.filter(class_id=subject_model.class_id, batch_id=batch_model)
    attendance = Attendance.objects.filter(class_id=class_model, batch_id=batch_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "batch_id":attendance_single.batch_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    batch_id = request.POST.get('batch')
    batch_obj = SectionOrBatch.objects.get(id=batch_id)
    date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
    attendance = Attendance.objects.get(attendance_date=date,batch_id=batch_obj)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "student_id":student.student_id.id ,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'admin_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def teacher_profile(request):
    pass


def student_profile(requtest):
    pass

def StudentPayment(request):
    
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()

    context = {
        'classes':classes ,
        'batches':batches ,
        
    }
    return render(request, 'admin_template/students_payment.html', context)
from django.db.models import Sum

@csrf_exempt
def StudentPaymentSingle(request):
    
    student_id = request.POST.get("student_id")
    studentCU = CustomUser.objects.get(id=student_id)
    stnd_obj = Students.objects.get(admin=studentCU)

    payment_data = FeesReport.objects.filter(student_id=stnd_obj).order_by("-fees_date")
    paid_at = []
    for i in payment_data:
        try:
            firstDate = i.paid_at
            date = datetime.strftime(firstDate,"%d %B,%Y")
            paid_at.append(date)
        except:
            none = ""
            paid_at.append(none)
    payment_data_values=payment_data.values()
    payment_details = list(payment_data_values)
    

   
    total_fees_dict = payment_data.aggregate(Sum('amount'))
    prevtotalAmount = list(total_fees_dict.values())[0]
    tAdAmount = payment_data.aggregate(Sum('extra_amount'))
    tAdAmountList =  list(tAdAmount.values())[0]
    totalAmount = int(prevtotalAmount) + int(tAdAmountList)
    
    paid = FeesReport.objects.filter(student_id=stnd_obj,paid_status=1)
    total_paid_dict = paid.aggregate(Sum('amount'))
    paidAmount = list(total_paid_dict.values())[0]
    
    try:
        paidAmount = int(paidAmount)
    except:
        paidAmount = 0

    try:
        dueAmount = totalAmount - paidAmount
    except:
        dueAmount = 0



    return JsonResponse({'status':'OK', 'payment_details':payment_details , 'paid_at' :paid_at,'totalAmount':totalAmount , 'paidAmount':paidAmount , 'dueAmount':dueAmount})
       

@csrf_exempt
def get_students_fees(request):
    # Getting Values from Ajax POST 'Fetch Student'
    class_id = request.POST.get("classes")
    batch = request.POST.get("batch")
    fees_month = request.POST.get("date")
    
    fees_actual_date = str(fees_month)+"-1"
    fees_date = datetime.strptime(fees_actual_date,'%Y-%m-%d').date()

    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    class_model = Classes.objects.get(id=class_id)

    batch_model = SectionOrBatch.objects.get(id=batch)

    students = Students.objects.filter(class_id=class_model, batch_id=batch_model  , active_status = True)
    # Only Passing Student Id and Student Name Only
    list_data = []

    # fees = FeesReport.objects.filter(fees_date = fees_date).exists()
    # if fees:
    #     feesR = FeesReport.objects.filter(fees_date = fees_date)
    # for i in feesR:
    for student in students:
        try:
            feesreport = FeesReport.objects.get(fees_date = fees_date , student_id = student)
            data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name ,"color":"danger" , "fees":student.feesAmount}
            list_data.append(data_small)
        except:
            data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name ,"color":"success" , "fees":student.feesAmount}
            list_data.append(data_small)
    # else:
    #     for student in students:
    #         data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name ,"color":"danger" , "fees":student.feesAmount}
    #         list_data.append(data_small)
    
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



def take_fees(request):
    classes = Classes.objects.all()
    batch = SectionOrBatch.objects.all()
    context = {
        "classes": classes,
        "batches": batch
    }
    return render(request, "admin_template/take_fees_template.html", context)




@csrf_exempt
def save_fees_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    students_ids = request.POST.get("students_ids")
    class_id = request.POST.get("class_id")

    fees_title = request.POST.get("fees_title")
    fees_month = request.POST.get("fees_date")
    amount = request.POST.get("amount")
    batch_id = request.POST.get("batch_id")
    additional_amount = request.POST.get("additional_amount")
    additional_title = request.POST.get("additional_title")

    class_model = Classes.objects.get(id=class_id)
    batch_model = SectionOrBatch.objects.get(id=batch_id)

    json_student = json.loads(students_ids)
    # print(dict_student[0]['id'])
    # print(fees_date)
    
    # 2021-11
    fees_actual_date = str(fees_month)+"-1"
    fees_date = datetime.strptime(fees_actual_date,'%Y-%m-%d').date()
    # print(student_ids)
    try:
        

        for stud in json_student:
        
            
            student = Students.objects.get(admin=stud['id'])
            stat = stud['status']
            if stat == 1:
                fees_report = FeesReport(student_id=student,class_id=class_model, fees_date=fees_date,paid_status=0,action=0,fees_title=fees_title,batch_id=batch_model,amount=student.feesAmount,extra_fees_title=additional_title,extra_amount=additional_amount,status=stud['status'])
                fees_report.save()
                # phoneNumber = "88"+str(student.mobile)+",88"+str(student.fathersMobile)+",88"+str(student.mothersMobile)
                # message_body = "সম্মানিত অভিভাবক, আগামী ১০ তারিখের মধ্যে "+student.admin.first_name+" "+student.admin.last_name+"("+student.username+")"+" "+fees_title +" সংশ্লিষ্ট "+ amount +" টাকা পরিশোধ করার জন্য বিশেষ ভাবে অনুরোধ করা হলো ।  ধন্যবাদান্তে , Alim's Academy "
                # url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

                # payload  = {}
                # headers = {
                # 'Content-Type': 'application/x-www-form-urlencoded'
                # }

                # #response = requests.request("POST", url, headers=headers, data = payload)

                # print(response.text.encode('utf8'))
                # print(url)
            elif stat == 0:
                pass
           
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


##############################










def update_fees(request):
    classes = Classes.objects.all()
    batch = SectionOrBatch.objects.all()
    context = {
        "classes": classes,
        "batch": batch
    }
    return render(request, "admin_template/update_fees_template.html", context)










@csrf_exempt
def get_fees_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    class_id = request.POST.get("class")
    batch = request.POST.get("batch_id")

    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    class_model = Classes.objects.get(id=class_id)

    batch_model = SectionOrBatch.objects.get(id=batch)

    # students = Students.objects.filter(class_id=subject_model.class_id, batch_id=batch_model)
    fees = FeesReport.objects.filter(class_id=class_model, batch_id=batch_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for fees_single in fees:
        data_small={"id":fees_single.id, "fees_date":str(fees_single.fees_date), "batch_id":fees_single.batch_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)









@csrf_exempt
def get_fees_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    fees_date = request.POST.get('fees_date')
    fees = FeesReport.objects.get(id=fees_date)

    fees_data = FeesReport.objects.filter(fees_id=fees)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in fees_data:
        
        data_small={"id":student.student_id.admin.id, "amount":student.fees_id.amount , "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)
        

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)





@csrf_exempt
def update_fees_data(request):
    students_ids = request.POST.get("students_ids")

    fees_date = request.POST.get("fees_date")
    fees = FeesReport.objects.get(id=fees_date)

    json_student = json.loads(students_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            fees_report = FeesReport.objects.get(student_id=student, fees_id=fees)
            fees_report.status=stud['status']

            fees_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")







def teacher_payment_date_filter(request):

    teachers = Teachers.objects.all() # Getting the Subjects of class Enrolled
    context = {
        "teachers": teachers
    }
    return render(request, "admin_template/teacher_payment_date_filter.html", context)
@csrf_exempt
def teacher_payment_date_all(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_payment_date_filter')
    else:
        
        if request.POST.get('start_date') == "" or request.POST.get('end_date') == "":
            teacher_id = request.POST.get("teachers")
            payment_data = TeacherPaymentSerializer(Payment_Teacher.objects.filter(teacher_id=teacher_id).order_by('-payment_upto'),many=True).data
            payment_type = Teachers.objects.get(id=teacher_id).monthly_payment_type
            registered_classes_data = RegisteredClassSerializer(ClassAndPayment.objects.filter(teacher_id=teacher_id).order_by('-class_date'),many=True).data
        else:
            start_date = datetime.strptime(request.POST.get("start_date"),'%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST.get("end_date"),'%Y-%m-%d').date()

            teacher_id = request.POST.get("teachers")
            payment_data = TeacherPaymentSerializer(Payment_Teacher.objects.filter(teacher_id=teacher_id,payment_upto__range=(start_date,end_date)).order_by('-payment_upto'),many=True).data
            payment_type = Teachers.objects.get(id=teacher_id).monthly_payment_type
            registered_classes_data = RegisteredClassSerializer(ClassAndPayment.objects.filter(teacher_id=teacher_id,class_date__range=(start_date,end_date)).order_by('-class_date'),many=True).data

        return JsonResponse({'status':'Save','payment_data':payment_data,'payment_type':payment_type, 'registered_classes_data':registered_classes_data})

@csrf_exempt
def teacher_payment_all(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_payment_date_filter')
    else:
        try:
            
            teacher_id = request.POST.get("teachers")
               
            try:
                payment_details = Payment_Teacher.objects.filter(teacher_id=teacher_id).order_by('-payment_upto')

                payment_details_values = payment_details.values()

                payment_data = list(payment_details_values)


                teacher_obj = Teachers.objects.get(id=teacher_id)
            
                approved_class = ClassAndPayment.objects.filter(teacher_id=teacher_obj,status=1).order_by('-class_date')

                approved_class_values = approved_class.values()

                approved_class_data = list(approved_class_values)

                    
                total_payment_dict = approved_class.aggregate(Sum('per_class_charge'))

                total_payment_list_value = list(total_payment_dict.values())[0]
                
                
                
                
                paid_payment_dict = payment_details.aggregate(Sum('payment_amount'))
                paid_payment_list_value = list(paid_payment_dict.values())[0]

                due_payment = total_payment_list_value - paid_payment_list_value

                return JsonResponse({'status':'Save','payment_data' : payment_data,'approved_class_data':approved_class_data , 'total_payment_list_value':total_payment_list_value,'paid_payment_list_value':paid_payment_list_value,'due_payment':due_payment})

            except:
                return JsonResponse({'status':'None'})

        except:
            messages.error(request, "Failed to Fetch Details . Check dates Correctly!!")
            return redirect('teacher_payment_date_filter')



@csrf_exempt
def teacher_payment_date_filter_single(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_payment_date_filter')
    else:

        start_date = datetime.strptime(request.POST.get("start_date"),'%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST.get("end_date"),'%Y-%m-%d').date()

        teacher_id = request.POST.get("teachers")
        payment_data = TeacherPaymentSerializer(Payment_Teacher.objects.filter(teacher_id=teacher_id,payment_upto__range=(start_date,end_date)).order_by('-payment_upto'),many=True).data
        payment_type = Teachers.objects.get(id=teacher_id).monthly_payment_type
        registered_classes_data = RegisteredClassSerializer(ClassAndPayment.objects.filter(teacher_id=teacher_id,class_date__range=(start_date,end_date)).order_by('-class_date'),many=True).data

        return JsonResponse({'status':'Save','payment_data':payment_data,'payment_type':payment_type, 'registered_classes_data':registered_classes_data})


def manage_teacher_single(request , teacher_id):

    teacher_obj = Teachers.objects.get(id=teacher_id)    
    # cust_id = Teachers.objects.get()    
    teacher_pcc = PCC.objects.filter(teacher_id=teacher_obj.admin.id)        
    total_class_taken = ClassAndPayment.objects.filter(teacher_id=teacher_obj).count()
    classNdPayment = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)
    total_earning_dict = classNdPayment.aggregate(Sum('per_class_charge'))
    total_earning_list_value = list(total_earning_dict.values())[0]                
    teacherPayment = Payment_Teacher.objects.filter(teacher_id=teacher_obj).order_by('-payment_upto')    
    total_paid_dict = teacherPayment.aggregate(Sum('payment_amount'))
    total_paid_dict_value = list(total_paid_dict.values())[0]

    classNPayment = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1).order_by('-class_date')[:3]
    teacherPymnt = Payment_Teacher.objects.filter(teacher_id=teacher_obj).order_by('-payment_upto')[:3]    
                

    context = {
        "total_paid_dict_value" : total_paid_dict_value ,
        "total_earning_list_value" : total_earning_list_value ,
        "total_class_taken" : total_class_taken ,
        "teacher_pcc" : teacher_pcc ,
        "classNPayment" : classNPayment ,
        "teacherPymnt" : teacherPymnt ,
        
        "teacher_obj" : teacher_obj ,
    }

    return render(request, 'admin_template/manage_teacher_single.html', context)




  

def manage_student_single(request , student_id):

    student_obj = Students.objects.get(id=student_id)    
    # cust_id = Teachers.objects.get()    
    examinations = Examination.objects.filter(class_id=student_obj.class_id.id,batch_id=student_obj.batch_id.id).last()
    # student_result = StudentResult.objects.filter(exam_id=examinations.id,student_id=student_obj.id)
  

    context = {
       
        "examinations":examinations,
        # "student_result" : student_result,
        "student_obj" : student_obj ,
    }

    return render(request, 'admin_template/manage_student_single.html', context)


    # return render(request,"student_template/online_class.html",context)

def view_result(request):
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()

    context = {
        "classes" : classes ,
        "batches" : batches ,
        
    }
    return render(request,"admin_template/view_result.html",context)







@csrf_exempt
def get_student_report(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_result')
    else:
                    
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        user_id = request.POST.get("student_id")
        
        student = Students.objects.get(admin=user_id)
        print(student.id)
        
        start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()

        examinations = Examination.objects.filter(class_id=student.class_id.id , status=1 , batch_id=student.batch_id.id, exam_date__range=(start_date_parse, end_date_parse)).order_by("-exam_date")
        examinations_values = examinations.values()
        examinations_data = list(examinations_values)


        student_result = StudentResult.objects.filter(student_id=student.id).order_by("-exam_id")
        student_result_values = student_result.values()
        student_result_data = list(student_result_values)

        list1 = []
        for i in student_result:
            st = StudentResult.objects.get(id=i.id)
            
            list1.append(st.exam_id.id)

        subjectNamelist = []
        for i in student_result:
            st = StudentResult.objects.get(id=i.id)
            
            subjectNamelist.append(st.subject_id.subject_name)
        

        totalWorkingDay = AttendanceReport.objects.filter(student_id=student.id , created_at__range=(start_date_parse , end_date_parse)).count()
        totalPresent = AttendanceReport.objects.filter(student_id=student.id , status=True, created_at__range=(start_date_parse , end_date_parse)).count()
        totalAbsent = AttendanceReport.objects.filter(student_id=student.id , status=False, created_at__range=(start_date_parse , end_date_parse)).count()

        list2 = [totalWorkingDay,totalPresent,totalAbsent]

        totalMarks = TotalMarks.objects.filter(student_id=student.id, status=1 ,exam_date__range=(start_date_parse , end_date_parse)).order_by("-exam_id")

        tmVal = totalMarks.values()
        tmlist = list(tmVal)


        totalMarksDict = totalMarks.aggregate(Sum('total_marks'))
        totalMarksVal = list(totalMarksDict.values())[0]

        obtainedMarksDict = totalMarks.aggregate(Sum('obtained_marks'))
        obtainedMarksVal = list(obtainedMarksDict.values())[0]

        totalMarksIDList = []
        
        for i in totalMarks:
            j = i.exam_id.id
            totalMarksIDList.append(j)

            

        return JsonResponse({'status':'OK','subjectNamelist':subjectNamelist ,'list2':list2,'totalMarksIDList':totalMarksIDList ,'tmlist':tmlist,'totalWorkingDay':totalWorkingDay, 'totalMarksVal':totalMarksVal,'obtainedMarksVal':obtainedMarksVal ,'totalPresent':totalPresent,'totalAbsent':totalAbsent , 'student_result_data':student_result_data,'list1':list1 ,'examinations_data':examinations_data})


@csrf_exempt
def get_student_search(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('view_result')
    else:
        studentSearch = request.POST.get("studentSearch")
        

        students = CustomUser.objects.filter(first_name__icontains=studentSearch , user_type=3) | CustomUser.objects.filter(username__icontains=studentSearch , user_type=3 )
        studentsVal = students.values()
        studentslist = list(studentsVal)
        classDetails = []
        for i in students:
            id = i.id
            student = Students.objects.get(admin=id)
            gender = student.gender
            address = student.presentAddress
            profile_pic = "null"
            className = student.class_id.class_name
            batchName = student.batch_id.batch_name
            id = student.id
            classDetails = []
            data = {
                "id" : id ,
                "gender" : gender ,
                "address" : address ,
                "profile_pic" : profile_pic ,
                "className" : className ,
                "batchName" : batchName ,
            }
            classDetails.append(data)
        return JsonResponse({'status':'OK', "classDetails":classDetails , 'studentslist':studentslist})

def expenses(request):
    paymentTeacher = Payment_Teacher.objects.all().order_by('-payment_upto')
    paymentStudent = FeesReport.objects.filter(paid_status=1).order_by("-paid_at")
    additionalExpenses = AdditionalExpenses.objects.all().order_by("-date")
    totalUnpaid = ClassAndPayment.objects.filter(status=1)
    
    totalUnpaidAmount = totalUnpaid.aggregate(Sum('per_class_charge'))
    totalUnpaidlists = list(totalUnpaidAmount.values())[0]
    try:
        totalUnpaidlist = int(totalUnpaidlists)
    except:
        totalUnpaidlist = 0
    
    totalpaid = paymentTeacher.aggregate(Sum('payment_amount'))
    totalpaidlists = list(totalpaid.values())[0]

    totalRpayment = FeesReport.objects.filter(paid_status = 0)
    totalradditional = totalRpayment.aggregate(Sum('extra_amount'))
    totalradditionalamounts = list(totalradditional.values())[0]
    totalr = totalRpayment.aggregate(Sum('amount'))
    totalRamounts = list(totalr.values())[0]
    try:
        totalRamount = int(totalRamounts) + int(totalradditionalamounts)
    except:
        totalRamount = 0

    totalobtained = paymentStudent.aggregate(Sum('amount'))
    totalobtainedlists = list(totalobtained.values())[0]
    additionalobtained = paymentStudent.aggregate(Sum('extra_amount'))
    additionalobtainedlistts = list(additionalobtained.values())[0]
    try:
        totalobtainedlist = int(totalobtainedlists) + int(additionalobtainedlistts)
        
    except:
        totalobtainedlist = 0
        
        
    try:
        totalpaidlist = int(totalpaidlists)
    except:
        totalpaidlist = 0
    
    
    totalAE = additionalExpenses.aggregate(Sum('amount'))
    totalAElist1 = list(totalAE.values())[0]
    try:
        totalAElist = int(totalAElist1)
    except:
        totalAElist = 0
    
    try:
        totalexpenses = int(totalpaidlist) + int(totalAElist)
    except:
        totalexpenses = 0
    totalDueAmount = totalUnpaidlist - totalpaidlist
    
    totalprofit = totalobtainedlist - totalexpenses
    
    
    context = {
        'totalprofit' : totalprofit ,
        'totalexpenses' : totalexpenses ,
        'totalAElist':totalAElist ,
        'totalobtainedlist' : totalobtainedlist ,
        'totalpaidlist' : totalpaidlist ,
        'additionalExpenses' : additionalExpenses ,
        'paymentTeacher' : paymentTeacher ,
        'paymentStudent' : paymentStudent ,
        'totalDueAmount' : totalDueAmount ,
        'totalRamount' : totalRamount ,
    }
    return render(request,"admin_template/expenses.html",context)
@csrf_exempt
def add_expenses(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect(reverse('expenses'))
    else:
        try:
            expenseAmount = request.POST.get('expenseAmount')
            expenseDate  = request.POST.get('expenseDate')
            expenseTitle = request.POST.get('expenseTitle')           
            
            expenses = AdditionalExpenses(title=expenseTitle , date=expenseDate , amount=expenseAmount)
            expenses.save()
            return HttpResponse("True")

        except:
            return HttpResponse("False")
    
@csrf_exempt
def get_expenses(request):
    
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    
    start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    paymentTeacher = Payment_Teacher.objects.filter(payment_upto__range=(start_date_parse , end_date_parse)).order_by('-payment_upto')
    paymentTeacherValues = paymentTeacher.values()
    paymentTeacherList = list(paymentTeacherValues)

    paymentStudent = FeesReport.objects.filter(paid_status=1,fees_date__range=(start_date_parse , end_date_parse)).order_by("-paid_at")

    paymentStudentValues = paymentStudent.values()

    paymentStudentList = list(paymentStudentValues)
    
    total_recieved = FeesReport.objects.filter(paid_status=1 , paid_at__range=(start_date_parse , end_date_parse)).order_by("paid_at")
    total_recieved_val = total_recieved.values()
    total_recieved_list = list(total_recieved_val)
    
    totalRecieved = total_recieved.aggregate(Sum('amount'))
    totalAdditionalRecieved = total_recieved.aggregate(Sum('extra_amount'))
    totalRAmounts = list(totalRecieved.values())[0] 
    totalRAdditionalAmount =  list(totalAdditionalRecieved.values())[0]
    try:
        totalRecievedAmount = int(totalRAmounts) + int(totalRAdditionalAmount)
    except:
        totalRecievedAmount = 0
    
    additionalExpenses = AdditionalExpenses.objects.filter(date__range=(start_date_parse , end_date_parse)).order_by("-date")
  
    totalRpayment = FeesReport.objects.filter(paid_status=0 , fees_date__range=(start_date_parse , end_date_parse))
    totalr = totalRpayment.aggregate(Sum('amount'))
    totalrAdditional = totalRpayment.aggregate(Sum('extra_amount'))
    totalRamountsAdditional = list(totalrAdditional.values())[0] 
    totalRamounts = list(totalr.values())[0]
    try:
        totalRamount = int(totalRamounts) + int(totalRamountsAdditional)
    except:
        totalRamount = 0

    
    pt = Payment_Teacher.objects.filter(payment_upto__range=(start_date_parse , end_date_parse)).order_by('-payment_upto')
    ptList = []
    for i in pt:
        teacher_name = Teachers.objects.get(id=i.teacher_id.id)
        ptList.append(teacher_name.admin.first_name+" "+teacher_name.admin.last_name)
    
    st = FeesReport.objects.filter(paid_status=1,fees_date__range=(start_date_parse , end_date_parse))
    stList = []
    for i in st:
        student_name = Students.objects.get(id=i.student_id.id)
        stList.append(student_name.admin.first_name+" "+student_name.admin.last_name)
    paid_st_list = []
    for i in total_recieved:
        student_name = Students.objects.get(id=i.student_id.id)
        paid_st_list.append(student_name.admin.first_name+" "+student_name.admin.last_name)
    
    expenses = AdditionalExpenses.objects.filter(date__range=(start_date_parse , end_date_parse))
    expensesValues = expenses.values()
    expensesList = list(expensesValues)
    
    totalpaid = paymentTeacher.aggregate(Sum('payment_amount'))
    totalpaidlists = list(totalpaid.values())[0]

    totalobtained = paymentStudent.aggregate(Sum('amount'))
    totalobtainedadditional = paymentStudent.aggregate(Sum('extra_amount'))
    totalobtainedlists = list(totalobtained.values())[0]  
    totaladditionaobtained = list(totalobtainedadditional.values())[0]
    
    totalAE = additionalExpenses.aggregate(Sum('amount'))
    totalAElist = list(totalAE.values())[0]
    
    try:
        totalobtainedlist = int(totalobtainedlists) + int(totaladditionaobtained)
        
    except:
        totalobtainedlist = 0
        
        
    try:
        totalpaidlist = int(totalpaidlists)
    except:
        totalpaidlist = 0
    
    totalAE = additionalExpenses.aggregate(Sum('amount'))
    totalAElist = list(totalAE.values())[0]
    
    try:
        totalexpenses = int(totalpaidlist) + int(totalAElist)
    except:
        totalexpenses = 0

    
    totalprofit = totalobtainedlist - totalexpenses
    
    totalUnpaid = ClassAndPayment.objects.filter(status=1 , class_date__range=(start_date_parse , end_date_parse))
    
    totalUnpaidAmount = totalUnpaid.aggregate(Sum('per_class_charge'))
    totalUnpaidlists = list(totalUnpaidAmount.values())[0]
    try:
        totalUnpaidlist = int(totalUnpaidlists)
    except:
        totalUnpaidlist = 0
    totalDueAmount = totalUnpaidlist - totalpaidlist

    return JsonResponse({'status':'OK', 'ptList':ptList , 'paid_st_list':paid_st_list ,'total_recieved_list': total_recieved_list  , 'totalRecievedAmount':totalRecievedAmount , 'totalRamount' : totalRamount , 'totalDueAmount':totalDueAmount , 'totalprofit':totalprofit ,'totalobtainedlist':totalobtainedlist , 'totalexpenses':totalexpenses , 'totalAElist':totalAElist , 'totalpaidlist':totalpaidlist, 'stList':stList ,'expensesList':expensesList,'paymentStudentList':paymentStudentList ,'paymentTeacherList':paymentTeacherList})

def single_notice(request,notice_id):
    notice = Notices.objects.get(id=notice_id)
    context={
        "notice":notice
    }
    return render(request,"admin_template/single-notice.html",context)

def add_notice(request):
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    notices = Notices.objects.all()

    context = {
        "notices" : notices  ,
        "classes" : classes ,
        "batches" : batches ,
    }

    return render(request,"admin_template/add_notice.html",context)

def save_notice(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect(reverse('add_notice'))
    else:
        class_id = request.POST.get('classes')
        batch_id = request.POST.get('batches')
        title = request.POST.get('title')
        description = request.POST.get('description')

        clss = Classes.objects.get(id=class_id)
        batch = SectionOrBatch.objects.get(id=batch_id)
        students = Students.objects.filter(class_id=clss,batch_id=batch ,  active_status = True)
        
        # first = True
        for student in students:
            phoneNumber = "88"+str(student.smsMobile)
            message_body = "Notice From Alim's Academy! "+title+"   "+description
            url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

            payload  = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            #response = requests.request("POST", url, headers=headers, data = payload)

           
        notice = Notices(class_id=clss,batch_id=batch,title=title,description=description)        
        notice.save()
        return redirect(reverse('add_notice'))
        
        

def edit_notice(request, notice_id):
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    notices = Notices.objects.get(id=notice_id)

    context = {
        "notices" : notices ,
        "classes" : classes ,
        "batches" : batches ,

    }
    return render(request,"admin_template/edit_notice.html",context)
def edit_notice_save(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('add_notice')
    else:
        notice_id = request.POST.get('notice_id')
        class_id = request.POST.get('classes')
        batch_id = request.POST.get('batches')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        notice = Notices.objects.get(id=notice_id)
        clss = Classes.objects.get(id=class_id)
        batch = SectionOrBatch.objects.get(id=batch_id)

        notice.title = title
        notice.description = description
        notice.class_id = clss
        notice.batch_id = batch
        notice.save()

        messages.success(request, "Notice Editted Successfully")
        return redirect('add_notice')

        
      

        

def delete_notice(request, notice_id):
    try:
        notice = Notices.objects.get(id=notice_id)
        notice.delete()

        messages.success(request, "Notice Deleted Successfully.")
        return redirect('add_notice')
    except:
        messages.error(request, "Failed to Delete Notice.")
        return redirect('add_notice')




def assign_subjects_to_teacher(request):
    pcc = PCC.objects.all()
    classes = Classes.objects.all()
    
    teachers = Teachers.objects.filter(active_status=True)
    
    context = {
        'pcc' : pcc ,
    
        'classes' : classes ,
    
        'teachers': teachers ,

    }

    return render(request,"admin_template/assign_subjects_to_teacher.html",context)


def assign_subjects_to_teacher_save(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return reverse('assign_subjects_to_teacher')
    else:
        try:
            teacher_id = request.POST.get('teachers')
            class_id = request.POST.get('classes')
            batch_id = request.POST.get('batches')
            subject_id = request.POST.get('subjects')
            amount = request.POST.get('amount')
    
            teacher_obj = Teachers.objects.get(id=teacher_id)
            teacher_obj_cu = CustomUser.objects.get(id=teacher_obj.admin.id)
            class_obj = Classes.objects.get(id=class_id)
            subject_obj = Subjects.objects.get(id=subject_id)
            batch_obj = SectionOrBatch.objects.get(id=batch_id)
    
            pcc = PCC(teacher_id=teacher_obj_cu,class_id=class_obj,batch_id=batch_obj,subject_id=subject_obj,amount=amount)
            pcc.save()
            message = "Successfully Assigned"+ " " + subject_obj.subject_name +" to " + teacher_obj.admin.first_name +" "+ teacher_obj.admin.last_name
            messages.success(request,message)
            return redirect('assign_subjects_to_teacher')
        except:
            messages.error(request,"Check your Credentials")
            return redirect('assign_subjects_to_teacher')

def edit_assigned_subjects_to_teacher(request, pcc_id):
    pcc = PCC.objects.get(id=pcc_id)
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    teachers = Teachers.objects.filter(active_status=True)
    subjects = Subjects.objects.all()
    context = {
        'pcc' : pcc ,
        'subjects' : subjects ,
        'classes' : classes ,
        'batches' : batches ,
        'teachers': teachers ,

    }
    return render(request,"admin_template/edit_assigned_subjects_to_teacher.html",context)

def edit_assigned_subjects_to_teacher_save(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return reverse('assign_subjects_to_teacher')
    else:
        try:
    
            teacher_id = request.POST.get('teachers')
            class_id = request.POST.get('classes')
            batch_id = request.POST.get('batches')
            subject_id = request.POST.get('subjects')
            amount = request.POST.get('amount')
            pcc_id = request.POST.get('pcc_id')
    
            teacher_obj = Teachers.objects.get(id=teacher_id)
            teacher_obj_cu = CustomUser.objects.get(id=teacher_obj.admin.id)
            class_obj = Classes.objects.get(id=class_id)
            subject_obj = Subjects.objects.get(id=subject_id)
            batch_obj = SectionOrBatch.objects.get(id=batch_id)
    
            pcc = PCC.objects.get(id=pcc_id)
            pcc.teacher_id = teacher_obj_cu
            pcc.class_id = class_obj
            pcc.batch_id = batch_obj
            pcc.subject_id = subject_obj
            pcc.amount = amount
            pcc.save()
            message = "Successfully Editted"+ " " + subject_obj.subject_name +" to " + teacher_obj.admin.first_name +" "+ teacher_obj.admin.last_name
            messages.success(request,message)
            return redirect('assign_subjects_to_teacher')
        except:
            messages.error(request,"Check your Credentials")
            return redirect('assign_subjects_to_teacher')

def delete_assigned_subjects_to_teacher(request , pcc_id):
    pcc = PCC.objects.get(id=pcc_id)
    pcc.delete()
    messages.success(request,"Successfully Deleted")
    return redirect('assign_subjects_to_teacher')
    

def add_exam(request):
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    exams = Examination.objects.all().order_by('-exam_date')
    studentResult = StudentResult.objects.all().order_by('-exam_id')
    


    context = {
        'studentResult':studentResult,
        'classes' : classes ,
        'batches' : batches ,
        'exams' : exams ,
    }
    return render(request ,"admin_template/add_exam.html",context)
def save_exam(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('add_exam')
    else:
        try:
            title = request.POST.get('title')
            date = request.POST.get('date')
            batch_id = request.POST.get('batch_id')
            class_id = request.POST.get('class_id')

            class_obj = Classes.objects.get(id=class_id)
            batch_obj = SectionOrBatch.objects.get(id=batch_id)

            exam = Examination(class_id=class_obj,batch_id=batch_obj,exam_name=title,exam_date=date)
            exam.save()
            messages.success(request,"Successfully Added Examination")
            return redirect('add_exam')
        except:
            messages.error(request,"Failed to Add Examination")
            return redirect('add_exam')

def edit_exam(request,exam_id):
    exams = Examination.objects.get(id=exam_id)
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    context = {
        'classes' : classes ,
        'batches' : batches ,
        'exams' : exams ,
    }
    return render(request ,"admin_template/edit_exam.html",context)

def edit_exam_save(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('add_exam')
    else:
        try:
            title = request.POST.get('title')
            date = request.POST.get('date')
            batch_id = request.POST.get('batch_id')
            class_id = request.POST.get('class_id')
            exam_id = request.POST.get('exam_id')

            class_obj = Classes.objects.get(id=class_id)
            batch_obj = SectionOrBatch.objects.get(id=batch_id)

            exam = Examination.objects.get(id=exam_id)
            exam.exam_name = title
            exam.exam_date = date
            exam.class_id = class_obj
            exam.batch_id = batch_obj

            exam.save()
            messages.success(request,"Successfully Editted Examination")
            return redirect('add_exam')
        except:
            messages.error(request,"Failed to Edit Examination")
            return redirect('add_exam')

def delete_exam(request,exam_id):
    exam = Examination.objects.get(id=exam_id)
    exam.delete()
    messages.error(request,"Successfully Deleted Examination")
    return redirect('add_exam')

def publish_result(request,exam_id):
    # try:
    exam = Examination.objects.get(id=exam_id)
    tm = TotalMarks.objects.filter(exam_id=exam.id)
    # phoneNumber = ""

    result = StudentResult.objects.filter(exam_id=exam_id)
    # first = True
    for r in result:
        
        phoneNumber = "88"+str(r.student_id.smsMobile)
        first_name = str(r.student_id.admin.first_name)
        last_name = str(r.student_id.admin.last_name)
        subject = str(r.subject_id.subject_name)
        totalMarks = str(r.subject_assignment_marks)
        examMarks = str(r.subject_exam_marks)
        # message_body = "Result of "+ first_name +" "+ last_name +" for " + exam.exam_name +" : "+subject+" : " + examMarks +"/"+totalMarks
        message_body = "নামঃ "+ first_name +" "+ last_name +"("+str(r.student_id.admin.username)+") পরীক্ষার নামঃ " + exam.exam_name +" বিষয়ঃ "+subject+"  প্রাপ্তনম্বরঃ " + examMarks +"/"+totalMarks
        url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

        payload  = {}
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        #response = requests.request("POST", url, headers=headers, data = payload)

        #print(response.text.encode('utf8'))
        print(url)
        
    for i in tm:
        i.status = 1
        i.save()
    exam.status = 1
    exam.save()




    # phoneNumber = "88"+str(mobile)+",88"+str(fathersMobile)+",88"+mothersMobile
    # message_body = "Welcome to Alim's Academy "+ first_name +" "+ last_name +"!! We are very Glad to have you as a valuable part of Our Institute. Your Login Details are given Below:"+ " Email : "+ str(email)+" Password :" +str(password) +""
    # url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

    # payload  = {}
    # headers = {
    # 'Content-Type': 'application/x-www-form-urlencoded'
    # }

    # #response = requests.request("POST", url, headers=headers, data = payload)

    # print(response.text.encode('utf8'))
    # print(url)
    messages.success(request,"Successfully Published Examination")
    return redirect('add_exam')
    # except:
    #     messages.error(request,"Failed to Publish Examination")
    #     return redirect('add_exam')






def add_accountant(request):
    return render(request, "admin_template/add_accountant_template.html")


def add_accountant_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_accountant')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        presentAddress = request.POST.get('presentAddress')
        parmanentAddress = request.POST.get('parmanentAddress')
        mobileNumber = request.POST.get('mobileNumber')
        emergencyMobileNumber = request.POST.get('emergencyMobileNumber')
        gender = request.POST.get('gender')
        
        dateOfBirth = request.POST.get('dateOfBirth')
        experience = request.POST.get('experience')
        
        

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
            user.accountants.presentAddress = presentAddress
            user.accountants.parmanentAddress = parmanentAddress
            user.accountants.mobileNumber = mobileNumber
            user.accountants.emergencyMobileNumber = emergencyMobileNumber
            user.accountants.gender = gender
            
            user.accountants.dateOfBirth = dateOfBirth
            user.accountants.experience = experience
            
            
            user.save()
            messages.success(request, "Accountant Added Successfully!")
            return redirect('add_accountant')
        except:
            messages.error(request, "Failed to Add Accountant!")
            return redirect('add_accountant')



def manage_accountant(request):
    accountants = Accountants.objects.all()
    context = {
        "accountants": accountants
    }
    return render(request, "admin_template/manage_accountant_template.html", context)


def edit_accountant(request, accountant_id):
    accountant = Accountants.objects.get(admin=accountant_id)
    date = accountant.dateOfBirth
    birthDate = datetime.strftime(date , "%Y-%m-%d")

    context = {
        "accountant": accountant,
        "id": accountant_id ,
        "birthDate":birthDate,
    }
    return render(request, "admin_template/edit_accountant_template.html", context)


  

def manage_accountant_single(request , accountant_id):

    accountant_obj = Accountants.objects.get(id=accountant_id)    
    
    
                

    context = {
        "accountant_obj" : accountant_obj ,
    }

    return render(request, 'admin_template/manage_accountant_single.html', context)





def edit_accountant_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        accountant_id = request.POST.get('accountant_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        presentAddress = request.POST.get('presentAddress')
        parmanentAddress = request.POST.get('parmanentAddress')
        mobileNumber = request.POST.get('mobileNumber')
        emergencyMobileNumber = request.POST.get('emergencyMobileNumber')
        gender = request.POST.get('gender')
        
        dateOfBirth = request.POST.get('dateOfBirth')
        experience = request.POST.get('experience')
        
        
        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=accountant_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            if password != None and password != "":
                user.set_password(password)
                accountant = Accountants.objects.get(admin=user.id)
                phoneNumber = "88"+accountant.mobileNumber
                message_body = "Congratulations!Your Password Have been Changed by the Authourity. Your New Login Details are given below : Username: "+ user.username +" Password: "+ password+" . Best Regards Alim's Academy"
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""
    
                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
    
                #response = requests.request("POST", url, headers=headers, data = payload)

            user.save()
            
            # INSERTING into teacher Model
            accountant_model = Accountants.objects.get(admin=accountant_id)
            
            accountant_model.presentAddress = presentAddress
            accountant_model.parmanentAddress = parmanentAddress
            accountant_model.mobileNumber = mobileNumber
            accountant_model.emergencyMobileNumber = emergencyMobileNumber
            accountant_model.gender = gender
            
            accountant_model.dateOfBirth = dateOfBirth
            accountant_model.experience = experience
            
            accountant_model.save()

            messages.success(request, "Accountant Updated Successfully.")
            return redirect('/edit_accountant/'+accountant_id)

        except:
            messages.error(request, "Failed to Update accountant.")
            return redirect('/edit_accountant/'+accountant_id)



def delete_accountant(request, accountant_id):
    accountant = Accountants.objects.get(admin=accountant_id)
    try:
        accountant.delete()
        messages.success(request, "Accountant Deleted Successfully.")
        return redirect('manage_accountant')
    except:
        messages.error(request, "Failed to Delete accountant.")
        return redirect('manage_accountant')
@csrf_exempt
def get_student_batch_search(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('view_result')
    else:
        class_id = request.POST.get("class_id")
        batch_id = request.POST.get("batch_id")

        class_obj = Classes.objects.get(id=class_id)
        batch_obj = SectionOrBatch.objects.get(id=batch_id)

        students = Students.objects.filter(class_id=class_obj,batch_id=batch_obj , active_status = True)

        studentsVal = students.values()
        studentslist = list(studentsVal)
        studentData = []
        for i in students:
            className = i.class_id.class_name
            batchName = i.batch_id.batch_name
            last_login = i.admin.last_login
            date_joined = i.admin.date_joined
            
            
            details = {
                "className" : className ,
                "batchName" : batchName ,
                "last_login" : last_login ,
                "date_joined" : date_joined ,
                
            }
            studentData.append(details)

        studentsNameList = []
        for i in students:
            studentsName = i.admin.first_name + " " + i.admin.last_name
            studentsNameList.append(studentsName)
        studentsUsernameList = []
        for i in students:
            studentsUsername = i.admin.username
            studentsUsernameList.append(studentsUsername)
        studentsEmailList = []
        for i in students:
            studentsEmail = i.admin.email
            studentsEmailList.append(studentsEmail)

        studentsAdminIDList = []
        for i in students:
            studentsAdminID = i.admin.id
            studentsAdminIDList.append(studentsAdminID)
        # studentsEmailList = []
        # for i in students:
        #     studentsEmail = i.admin.email
        #     studentsEmailList.append(studentsEmail)

        return JsonResponse({'status':'OK', 'studentsAdminIDList':studentsAdminIDList, "studentData":studentData, 'studentsEmailList':studentsEmailList , 'studentsUsernameList':studentsUsernameList ,'studentsNameList':studentsNameList,'studentslist':studentslist})

def student_payment_batch_filter(request):
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    context = {
        'classes' : classes ,
        'batches' : batches ,
    }
    return render(request,"admin_template/batch_payment.html",context)
@csrf_exempt
def get_filter_payment_all(request):
    class_id = request.POST.get('classes')
    batch_id = request.POST.get('batch')

    class_obj = Classes.objects.get(id=class_id)
    batch_obj = SectionOrBatch.objects.get(id=batch_id)
    
    payment = FeesReport.objects.filter(paid_status=1,class_id=class_obj,batch_id=batch_obj).order_by("-paid_at")
    paymentVal = payment.values()
    paymentList = list(paymentVal)

    studentIDList = []
    for i in payment:
        student_id = i.student_id.id
        studentIDList.append(student_id)
    coachingID=[]
    for i in payment:
        id = i.student_id.admin.username
        coachingID.append(id)
    dates = []
    for i in payment:
        try:
            date = i.paid_at
            dates.append(datetime.strftime(date , "%d %B, %Y"))
        except:
            dates.append("None")

    studentList = []
    for i in payment:
        student_name = i.student_id.admin.first_name +" "+ i.student_id.admin.last_name
        studentList.append(student_name)
    

    return JsonResponse({'status':'OK','studentList':studentList , 'coachingID':coachingID ,'dates':dates , 'paymentList':paymentList ,'studentIDList':studentIDList})
@csrf_exempt
def get_unpaid_payments(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('student_payment_batch_filter')
    else:
        class_id = request.POST.get('classes')
        batch_id = request.POST.get('batch')
        class_obj = Classes.objects.get(id=class_id)
        batch_obj = SectionOrBatch.objects.get(id=batch_id)
        unpaids = FeesReport.objects.filter(batch_id=batch_obj , paid_status=0)
        unpaidVal = unpaids.values()
        unpaidDetails = list(unpaidVal)

        student_name = []
        for i in unpaids:
            name = i.student_id.admin.first_name +" "+ i.student_id.admin.last_name
            student_name.append(name)
        
        student_id = []
        for i in unpaids:
            id = i.student_id.id
            student_id.append(id)


        dates = []
        for i in unpaids:
            try:
                date = i.fees_date
                finalDate = datetime.strftime(date,"%d %B,%Y")
                dates.append(finalDate)
            except:
                dates.append("None")
        
        return JsonResponse({'status':'OK','unpaidDetails':unpaidDetails,'dates':dates,'student_name':student_name,'student_id':student_id })
def ask_for_payment(request,student_id,due):
    student_obj = Students.objects.get(id=student_id)
    phoneNumber = "88"+str(student_obj.smsMobile)
    # fathersMobile)+",88"+str(student_obj.mothersMobile)
    message_body = "সম্মানিত অভিভাবক, আপনার সন্তান "+ student_obj.admin.first_name +" "+ student_obj.admin.last_name +" এর "+ due +" ৳ টাকা বেতন বকেয়া রয়েছে । জরুরী ভিত্তিতে বেতন পরিশোধ করার জন্য বিশেষভাবে বলা হলো । ধন্যবাদান্তে , Alim's Academy "
    url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

    payload  = {}
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    #response = requests.request("POST", url, headers=headers, data = payload)

    #print(response.text.encode('utf8'))
    print(url)
    messages.success(request, "Message Sent Successfully!")
    return redirect('student_payment_batch_filter')    

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)

def download_teacher_invoice_view(request,payment_id):
    payments = Payment_Teacher.objects.get(id=payment_id)
    pdfDetails = PDFDetails.objects.all().last()
    now = datetime.now()
    
    mydict={
        'pdfDetails' : pdfDetails ,
        'payment' : payments ,
        'now' : now ,
    }
    
    return render_to_pdf('admin_template/teacher_payment_invoice.html',mydict)

@csrf_exempt
def download_student_report_card(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_result')
    else:
                    
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        user_id = request.POST.get("student_id")
        
        student = Students.objects.get(admin=user_id)
        print(student.id)
        
        start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()

        examinations = Examination.objects.filter(class_id=student.class_id.id , status=1 , batch_id=student.batch_id.id, exam_date__range=(start_date_parse, end_date_parse)).order_by("exam_date")

        student_result = StudentResult.objects.filter(student_id=student.id).order_by("exam_id")
        

        totalWorkingDay = AttendanceReport.objects.filter(student_id=student.id , created_at__range=(start_date_parse , end_date_parse)).count()
        totalPresent = AttendanceReport.objects.filter(student_id=student.id , status=True, created_at__range=(start_date_parse , end_date_parse)).count()
        totalAbsent = AttendanceReport.objects.filter(student_id=student.id , status=False, created_at__range=(start_date_parse , end_date_parse)).count()

        totalMarks = TotalMarks.objects.filter(student_id=student.id, status=1 ,exam_date__range=(start_date_parse , end_date_parse)).order_by("exam_id")


        totalMarksDict = totalMarks.aggregate(Sum('total_marks'))
        tmv = list(totalMarksDict.values())[0]


        obtainedMarksDict = totalMarks.aggregate(Sum('obtained_marks'))
        omv = list(obtainedMarksDict.values())[0]
        now = datetime.now()
        mydict={
            "exam":examinations,
            "result":student_result,
            "working":totalWorkingDay,
            "absent":totalAbsent,
            "present":totalPresent,
            "totalMarks":tmv,
            "obtainedMarks":omv,
            "student":student,
            "start":start_date_parse,
            "end":end_date_parse,
            "now":now
        }
            

        return render_to_pdf('admin_template/download_reportcard.html',mydict)


def download_invoice_view(request,payment_id):
    # order=models.Orders.objects.get(id=orderID)
    # product=models.Product.objects.get(id=productID)
    paymentStudent = FeesReport.objects.get(id=payment_id)
    pdfDetails = PDFDetails.objects.all().last()
    now = datetime.now()
    
    mydict={
        'pdfDetails' : pdfDetails ,
        'paymentStudent' : paymentStudent ,
        'now' : now ,
    }
    print(pdfDetails.img.url)
    return render_to_pdf('admin_template/download_invoice.html',mydict)
@csrf_exempt
def student_payment_batch_date_filter(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('student_payment_batch_filter')
    else:
        class_id = request.POST.get('classes')
        batch_id = request.POST.get('batch')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        class_obj = Classes.objects.get(id=class_id)
        batch_obj = SectionOrBatch.objects.get(id=batch_id)
        start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()

        fees_obj = FeesReport.objects.filter(class_id=class_obj,batch_id=batch_obj,paid_status=1, fees_date__range=(start_date_parse,end_date_parse))
        fees_obj_values = fees_obj.values()
        feesJson = list(fees_obj_values)

        studentJson = []
        for i in fees_obj:
            id = i.student_id.id
            student_obj = Students.objects.get(id=id)
            name = student_obj.admin.first_name +" "+ student_obj.admin.last_name
            username = student_obj.admin.username
            student_data = {
                "name" : name ,
                "coachingID" : username ,
            }
            studentJson.append(student_data)
        return JsonResponse({'status':'OK','studentJson':studentJson,'feesJson':feesJson})


def delete_payment(request,payment_id):
    try:

        fees = FeesReport.objects.get(id=payment_id)
        fees.paid_status = 0
        fees.action = 0
        fees.save()
        messages.success(request,"Payment Deleted Successfully!")
        return redirect('expenses')
    except:
        messages.error(request,"Some Error Occured!")
        return redirect('expenses')

def delete_expenses(request,expense_id):
    try:

        expense = AdditionalExpenses.objects.get(id=expense_id)
        expense.delete()
        expense.save()
        messages.success(request,"Expense Deleted Successfully!")
        return redirect('expenses')
    except:
        messages.error(request,"Some Error Occured!")
        return redirect('expenses')


@csrf_exempt
def get_student_by_coaching_id(request):
    # Getting Values from Ajax POST 'Fetch Student'
    coachingID = request.POST.get('coachingID')  
    
    studentCU = CustomUser.objects.get(username=coachingID)
    # students = Students.objects.get(admin=studentCU)

    details = []
    data = {
        "name" : studentCU.first_name+" "+studentCU.last_name ,
        "id" : studentCU.id
    }
    details.append(data)
    


    return JsonResponse({"status":"save" , "details":details})
    
def deactivate_student(request,student_id):
    student = Students.objects.get(admin=student_id)
    # customUser = CustomUser.objects.get(id=student.admin.id)
    try:
        student.active_status = False
        # customUser.is_active = False
        student.save()    
        # customUser.save()
        messages.info(request,"Successfully Deactivated Student")
        return redirect('manage_student')
    except:
        messages.warning(request,"Error in  Deactivating Student")
        return redirect('manage_student')




def re_activate_student(request,student_id):
    student = Students.objects.get(admin=student_id)
    
    try:
        student.active_status = True
        
        student.save()    
        
        messages.info(request,"Successfully Re-activated Student")
        return redirect('manage_student')
    except:
        messages.warning(request,"Error in  Reactivating Student")
        return redirect('manage_student')

def deactivate_teacher(request,teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
    
    try:
        teacher.active_status = False
        # customUser.is_active = False
        teacher.save()    
        # customUser.save()
        messages.success(request,"Successfully Deactivated Teacher")
        return redirect('manage_teacher')
    except:
        messages.error(request,"Error in  Deactivating Teacher")
        return redirect('manage_teacher')




def re_activate_teacher(request,teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
    
    try:
        teacher.active_status = True
        
        teacher.save()    
        
        messages.success(request,"Successfully Re-activated Teacher")
        return redirect('manage_teacher')
    except:
        messages.error(request,"Error in  Reactivating Teacher")
        return redirect('manage_teacher')
@csrf_exempt
def student_unpaid_date_filter(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('student_payment_batch_filter')
    else:

        class_id = request.POST.get('classes')
        batch_id = request.POST.get('batch')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        class_obj = Classes.objects.get(id=class_id)
        batch_obj = SectionOrBatch.objects.get(id=batch_id)
        # time = "00:01:00"
        start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()
        unpaids = FeesReport.objects.filter(class_id=class_obj,batch_id=batch_obj , paid_status=0 , fees_date__range=(start_date_parse,end_date_parse))
        unpaidVal = unpaids.values()
        unpaidDetails = list(unpaidVal)
        print(unpaidDetails)
        student_name = []
        for i in unpaids:
            name = i.student_id.admin.first_name +" "+ i.student_id.admin.last_name
            student_name.append(name)
        
        student_id = []
        for i in unpaids:
            id = i.student_id.id
            student_id.append(id)


        # dates = []
        # for i in unpaids:
        #     try:
        #         date = i.fees_date
        #         finalDate = datetime.strftime(date,"%d %B,%Y")
        #         dates.append(finalDate)
        #     except:
        #         dates.append("None")
        
        return JsonResponse({'status':'OK','unpaidDetails':unpaidDetails,'student_name':student_name,'student_id':student_id })



def exam_single(request,exam_id):
    exam = Examination.objects.get(id=exam_id)
    results = StudentResult.objects.filter(exam_id=exam)
    examName = exam.exam_name
    context = {
        "results" : results ,
        "examName" : examName ,
    }
    return render (request,"admin_template/exam_single.html",context)

def delete_single_result(request,result_id):
    # exam = Examination.objects.get(id=exam_id)
    results = StudentResult.objects.filter(id=result_id)
    results.delete()
    messages.success(request, " Successfully Deleted Result")
    return redirect('add_exam')
def manage_attendance(request):
    attendances = Attendance.objects.all().order_by("-attendance_date")
    details = {
        
        "attendances" : attendances ,
    }
    return render(request, "admin_template/manage_attendance.html",details)

def delete_attendance(request,attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
        attendance.delete()
        messages.success(request,"Successfully Deleted Attendance")
        return redirect('manage_attendance')
    except:
        messages.error(request,"Failed to Delete Attendance!")
        return redirect('manage_attendance')
        
def delete_student_payment(request,payment_id):
    try:
        payment = FeesReport.objects.get(id=payment_id)
        payment.action = 0
        payment.in_cash = 0
        payment.paid_status = 0
        payment.bkash_nmb = ""
        payment.trans_id = ""
        payment.paid_at = None
        payment.save()
        messages.success(request,"Successfully Deleted Payment")
        return redirect('student_payment_batch_filter')
    
    except:
        messages.error(request,"Failed to Delete Payment")
        return redirect('student_payment_batch_filter')
def delete_teacher_payment(request , payment_id):
    try:
        payment = Payment_Teacher.objects.get(id=payment_id)
        payment.delete()
        messages.success(request,"Successfully Deleted Payment")
        return redirect('teacher_payment_date_filter')
    except:
        messages.error(request,"Failed to  Payment")
        return redirect('teacher_payment_date_filter')
def delete_registered_class(request , reg_id):
    try:
        reg = ClassAndPayment.objects.get(id=reg_id)
        reg.delete()
        messages.success(request,"Successfully Deleted Registered Class")
        return redirect('teacher_class_reg')
    except:
        messages.error(request,"Failed to Regstered Class")
        return redirect('teacher_class_reg')
def manage_fees(request):
    classes = Classes.objects.all()
    fees = FeesReport.objects.all()
    context ={
        "classes" : classes ,
        "fees" : fees,
    }
    return render(request,"admin_template/manage_fees.html",context)
@csrf_exempt
def delete_fees(request):
    date1 = request.POST.get("fees")
    date = str(date1)+"-01"
    batch_id =request.POST.get("batch_id")
    fees_date = datetime.strptime(date,"%Y-%m-%d").date()
    batch_obj = SectionOrBatch.objects.get(id=batch_id)
    fees = FeesReport.objects.filter(batch_id=batch_obj,fees_date=fees_date)
    for i in fees:
        i.delete()
    return HttpResponse("OK")
@csrf_exempt
def load_fees(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('admin_home')
    else:
        date1 = request.POST.get("fees")
        date = str(date1)+"-01"
        batch_id =request.POST.get("batch_id")
        fees_date = datetime.strptime(date,"%Y-%m-%d").date()
        batch_obj = SectionOrBatch.objects.get(id=batch_id)
        fees = FeesReport.objects.filter(batch_id=batch_obj,fees_date=fees_date)
        feesVal = fees.values()
        feesList = list(feesVal)
        
        return JsonResponse({"status":"OK","feesList":feesList})
        
def admin_view_online_class(request):
    return render(request,"admin_template/online_class.html")
def get_admin_view_online_class(request):
    classes = OnlineClass.objects.all()
    online_class = OnlineClassSerializer(classes,many=True).data
    return JsonResponse({"status":"OK","data":online_class})

def sms(request):
    sms = CustomSMS.objects.all().order_by("-sent_at")
    
    context = {
        
        "sms" : sms ,
    }
    return render(request,"admin_template/sms.html",context)
    
@csrf_exempt
def sms_save(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
    else:
        numbers = request.POST.get("numbers")
        message = request.POST.get("message")
        sms = CustomSMS(number=numbers , message=message)
        
        sms.save()
        # phoneNumber = ""+ str(numbers) +""
        # message_body = ""+ str(message) +""
        url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ numbers +"&message="+ message +""

        payload  = {}
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        #response = requests.request("POST", url, headers=headers, data = payload)

        messages.success(request,"Successfully SMS Sent")
        return redirect('sms')
@csrf_exempt
def get_students_for_payment(request):
    batch = request.POST.get("batch")
    
    batch_model = SectionOrBatch.objects.get(id=batch)

    students = Students.objects.filter(batch_id=batch_model  , active_status = True)
    list_data = []
    for student in students:
        
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name ,"color":"danger" , "fees":student.feesAmount}
        list_data.append(data_small)
    
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    
    
    
def delete_student_payment_single(request , payment_id):
    payment = FeesReport.objects.get(id=payment_id)
    payment.delete()
    messages.success(request,"Successfully Deleted Payment")
    return redirect('manage_fees')
    
def notiofications(request):
    notifications = Notifications.objects.all().order_by("-created_at")
    context={
        "notifications":notifications
    }
    return render(request,"admin_template/notifications.html",context)
@csrf_exempt 
def get_not_number(request):
    notnmb = Notifications.objects.filter(status=False).count()
    notiofications = Notifications.objects.all().order_by("-created_at")
    list_data = []
    list_data.append({"notf":notnmb})
    l1 = notiofications.values()
    list2 = list(l1)      

    return JsonResponse({"notnmb":list_data,"notifications":list2})
@csrf_exempt     
def seen_all_notifications(request):
    notiofications = Notifications.objects.all().order_by("-created_at")
    for i in notiofications:
        i.status = True
        i.save()
    return JsonResponse({"status":"All Seen"})

    
@csrf_exempt 
def seen_notification(request,id):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
    else:
        # try:
        notification = Notifications.objects.get(id=id)
        notification.status = True
        notification.save()
        return JsonResponse({"status":"seen"})
        # except:
        #     return JsonResponse({"status":"error"})
    
def all_notifications(request):
    notifications = json.dumps(NotificationSerializer(Notifications.objects.all().order_by("-created_at"),many=True).data)
    return render(request,"admin_template/all_notifications.html",{"nots":notifications})