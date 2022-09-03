from datetime import datetime
from student_management_app.AdminViews import TeacherPayment
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.db.models import Sum

from student_management_app.models import CustomUser, Notifications, OnlineClass, Examination, PDFDetails, Teachers, Classes, Subjects, Students, SectionOrBatch, Attendance, AttendanceReport,  FeedBackTeachers, StudentResult ,  PCC , ClassAndPayment ,Payment_Teacher,TotalMarks


def teacher_home(request):
    # Fetching All Students under Teacher
    subjects = Subjects.objects.all()
    pccs = PCC.objects.filter(teacher_id=request.user.id)
    class_id_list= []
    for pcc in pccs:
        classes = Classes.objects.get(id=pcc.class_id.id)
        class_id_list.append(classes.id)
    
    final_class = []
    # Removing Duplicate class Id
    for class_id in class_id_list:
        if class_id not in final_class:
            final_class.append(class_id)
    
    students_count = Students.objects.filter(class_id__in=final_class,active_status=1).count()
    pcc_subjects = []
    for i in pccs:
        pcc_subjects.append(i.subject_id)

    subject_count = len(pcc_subjects)

    #Fetch Attendance Data by Subjects
    pccSubjects = pccs
    print(pccSubjects)
    
    teacher_obj = Teachers.objects.get(admin=request.user.id)
    approved_class = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)

        
    totalPayment = approved_class.aggregate(Sum('per_class_charge'))
    totalPaymentLists = list(totalPayment.values())[0]
      
    payment_data = Payment_Teacher.objects.filter(teacher_id=teacher_obj)
    
    total_payment_dict = payment_data.aggregate(Sum('payment_amount'))
    paidPaymentLists = list(total_payment_dict.values())[0]

    try:
        paidPaymentList = int(paidPaymentLists)
        
    except:
        paidPaymentList = 0
    
    try:
        totalPaymentList = int(totalPaymentLists)
    except:
        totalPaymentList = 0
    due_payment = totalPaymentList - paidPaymentList
    totalClass = ClassAndPayment.objects.filter(status=1 , teacher_id = teacher_obj).count()
    
    context={
        "totalClass" : totalClass ,
        "totalPaymentList" : totalPaymentList ,
        "paidPaymentList" : paidPaymentList ,
        "due_payment" : due_payment ,
        "students_count": students_count,
        "subject_count": subject_count,
        
    }
    return render(request, "teacher_template/teacher_home_template.html", context)



def teacher_take_attendance(request):
    # subjects = Subjects.objects.filter(teacher_id=request.user.id)
    batches = SectionOrBatch.objects.all()
    classes = Classes.objects.all()
    context = {
        "classes" : classes ,
        # "subjects": subjects,
        "batches": batches
    }
    return render(request, "teacher_template/take_attendance_template.html", context)


def teacher_class_register(request):
    try:
        pcc = PCC.objects.filter(teacher_id=request.user.id)
        # Classes = Classes.objects.all()
        # subject = Subjects.objects.filter(teacher_id=request.user.id)
        teacher_obj = Teachers.objects.get(admin=request.user.id)
        reg_data = ClassAndPayment.objects.filter(teacher_id=teacher_obj).order_by("-class_date")
        approved_class = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)

            
        ll = approved_class.aggregate(Sum('per_class_charge'))

        als = list(ll.values())[0]
        
        payment_data = Payment_Teacher.objects.filter(teacher_id=teacher_obj).order_by("-payment_upto")
        
        total_payment_dict = payment_data.aggregate(Sum('payment_amount'))
        total_payment_list_value = list(total_payment_dict.values())[0]
        try:
            al = int(als)
        except:
            al = 0
        try:
            total_payment_list_values = int(total_payment_list_value)
        except:
            total_payment_list_values = 0
        
        due_payment = al - total_payment_list_value
        context = {
            "due_payment" : due_payment,
            "payment_data" : payment_data,
            "tplv" : total_payment_list_value,
            "al" : al,
            # "classes" : classes ,
            # "subject" : subject ,
            "pcc" : pcc,
            "reg_data" : reg_data ,
            
        }
        return render(request, "teacher_template/teacher_class_reg_template.html", context)
    except:
        pcc = PCC.objects.filter(teacher_id=request.user.id)
        # Classes = Classes.objects.all()
        # subject = Subjects.objects.filter(teacher_id=request.user.id)
        teacher_obj = Teachers.objects.get(admin=request.user.id)
        reg_data = ClassAndPayment.objects.filter(teacher_id=teacher_obj).order_by("-class_date")
        approved_class = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1)

            
        ll = approved_class.aggregate(Sum('per_class_charge'))

        al = list(ll.values())[0]
        
        payment_data = Payment_Teacher.objects.filter(teacher_id=teacher_obj)
        
        total_payment_dict = payment_data.aggregate(Sum('payment_amount'))
        total_payment_list_value = list(total_payment_dict.values())[0]

        due_payment = 0
        context = {
            "due_payment" : due_payment,
            "payment_data" : payment_data,
            "tplv" : total_payment_list_value,
            "al" : al,
            # "classes" : classes ,
            # "subject" : subject ,
            "pcc" : pcc,
            "reg_data" : reg_data ,
            
        }
        return render(request, "teacher_template/teacher_class_reg_template.html", context)


def teacher_class_register_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_class_reg')
    else:
        try:
            pcc  = request.POST.get('pcc')
            amount = PCC.objects.get(id=pcc)
            class_date = request.POST.get('class_date')
            from_time = request.POST.get('from_time')
            to_time = request.POST.get('to_time')
            teacher_obj = Teachers.objects.get(admin=request.user.id)
            # try:
            reg_report = ClassAndPayment(teacher_id=teacher_obj,pcc_id=amount, per_class_charge=amount.amount, to_time=to_time , class_date=class_date,  from_time=from_time, status=0)
            reg_report.save()
            notifications = Notifications(title="A Class has been Registered by "+teacher_obj.admin.first_name+" "+teacher_obj.admin.last_name,link="/teacher_class_reg/",status=False)
            notifications.save()
            messages.success(request, "Applied for Class Registration.")
            return redirect('teacher_class_register')
        except:
            messages.error(request, "Failed to Apply Class Registration")
            return redirect('teacher_class_register')


def teacher_feedback(request):
    teacher_obj = Teachers.objects.get(admin=request.user.id)
    feedback_data = FeedBackTeachers.objects.filter(teacher_id=teacher_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "teacher_template/teacher_feedback_template.html", context)


def teacher_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('teacher_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        teacher_obj = Teachers.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackTeachers(teacher_id=teacher_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            notifications = Notifications(title="A New Report has been Sent by "+teacher_obj.admin.first_name+" "+teacher_obj.admin.last_name,link="/single_teacher_feedback/"+str(add_feedback.id),status=False)
            notifications.save()
            messages.success(request, "Feedback Sent.")
            return redirect('teacher_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('teacher_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    class_id = request.POST.get("class_id")
    # subject_id = request.POST.get("subject")
    batch = request.POST.get("batch")

    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    # subject_model = Subjects.objects.get(id=subject_id)

    batch_model = SectionOrBatch.objects.get(id=batch)

    class_model = Classes.objects.get(id=class_id)

    students = Students.objects.filter(class_id=class_model, batch_id=batch_model , active_status = True)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    
    

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    batch_id = request.POST.get("batch_id")
    class_id = request.POST.get("classes")

    # subject_model = Subjects.objects.get(id=subject_id)
    class_model = Classes.objects.get(id=class_id)
    batch_model = SectionOrBatch.objects.get(id=batch_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    # try:
    # First Attendance Data is Saved on Attendance Model
    attendance = Attendance(class_id=class_model,attendance_date=attendance_date, batch_id=batch_model)
    attendance.save()

    for stud in json_student:
        # Attendance of Individual Student saved on AttendanceReport Model
        student = Students.objects.get(admin=stud['id'])
        attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
        if stud['status'] == 0:
            phoneNumber = "88"+str(student.smsMobile)
            message_body = "নামঃ "+str(student.admin.first_name)+" "+str(student.admin.last_name)+" ID:"+str(student.admin.username)+" তারিখঃ "+attendance_date+" কোচিং ক্লাসে অনুপস্থিত ছিলো । "  
            url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

            payload  = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            #response = requests.request("POST", url, headers=headers, data = payload)

            #print(response.text.encode('utf8'))
            print(url)
            
            attendance_report.save()
        elif stud['status'] == 1:
            attendance_report.save()


    return HttpResponse("OK")
    # except:
    #     return HttpResponse("Error")




def teacher_update_attendance(request):
    classes = Classes.objects.all()
    context = {
        "classes": classes ,
        
    }
    return render(request, "teacher_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    
    class_id = request.POST.get("class_id")
    batch = request.POST.get("batch_id")
    

    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    
    class_model = Classes.objects.get(id=class_id)
    batch_model = SectionOrBatch.objects.get(id=batch)
    attendance = Attendance.objects.filter(class_id=class_model,batch_id=batch_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "batch_id":attendance_single.batch_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_student(request):
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
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    batch_id = request.POST.get('batch')
    batch_obj = SectionOrBatch.objects.get(id=batch_id)
    date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
    
    attendance = Attendance.objects.get(attendance_date=date,batch_id=batch_obj)
    
    json_student = json.loads(student_ids)

    # try:
    
    for stud in json_student:
        # Attendance of Individual Student saved on AttendanceReport Model
        student = Students.objects.get(admin=stud['id'])

        attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
        attendance_report.status=stud['status']

        attendance_report.save()
    return HttpResponse("OK")
    # except:
    #     return HttpResponse("Error")






def teacher_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=user)

    context={
        "user": user,
        "teacher": teacher
    }
    return render(request, 'teacher_template/teacher_profile.html', context)


def teacher_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('teacher_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
                teacher = Teachers.objects.get(admin=customuser.id)
                phoneNumber = "88"+teacher.mobileNumber
                message_body = "Congratulations!You Have Successfully Changed Your Password. Your New Login Details are given below : Username: "+ customuser.username +" Password: "+ password +" . Best Regards , Alim's Academy"
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""
    
                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
    
                #response = requests.request("POST", url, headers=headers, data = payload)

                
            customuser.save()

            teacher = Teachers.objects.get(admin=customuser.id)
            teacher.address = address
            teacher.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('teacher_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('teacher_profile')



def teacher_add_result(request):
    teacher_obj = CustomUser.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=teacher_obj)
    pcc = PCC.objects.filter(teacher_id=teacher_obj)
    result = StudentResult.objects.filter(teacher_id=teacher.id).order_by("-created_at")
    
    print(result)
    # batches = 
    # batches = SectionOrBatch.objects.all()
    context = {
        "pcc": pcc,
        "result" : result ,
        # "batches": batches,
    }
    return render(request, "teacher_template/add_result_template.html", context)


def teacher_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_add_result')
    else:
        student_admin_id = request.POST.get('student_id')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')
        exam_id = request.POST.get('exam')
        

        exam_obj = Examination.objects.get(id=exam_id)
        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

       

        # Check if Students Result Already Exists or not
        check_exist = StudentResult.objects.filter(subject_id=subject_obj, exam_id=exam_obj, student_id=student_obj).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=subject_obj, exam_id=exam_obj ,student_id=student_obj)
            check_total_marks_exist = TotalMarks.objects.filter(student_id=student_obj,exam_id=exam_obj).exists()
            if check_total_marks_exist:
                    totalMarks = TotalMarks.objects.get(student_id=student_obj,exam_id=exam_obj)
                    oldTotalMark = int(totalMarks.total_marks) - int(result.subject_assignment_marks)
                    oldObtainedMark = int(totalMarks.obtained_marks) - int(result.subject_exam_marks)
                    newObtianedMark = oldObtainedMark + int(exam_marks)
                    newTotalMark = oldTotalMark + int(assignment_marks)
                    totalMarks.obtained_marks = newObtianedMark
                    totalMarks.total_marks = newTotalMark
                    totalMarks.exam_date = exam_obj.exam_date
                    totalMarks.save()
            exam_fraction = int(exam_marks) / int(assignment_marks) 
            exam_percentage = int(exam_fraction * 100)
                       
            if exam_percentage >= 80:
                result.gpa = 5.00
            elif exam_percentage >= 70:
                result.gpa = 4.00
            elif exam_percentage >= 60:
                result.gpa = 3.50
            elif exam_percentage >= 50:
                result.gpa = 3.00
            elif exam_percentage >= 40:
                result.gpa = 2.00
            elif exam_percentage >= 33:
                result.gpa = 1.00
            elif exam_percentage < 33 :
                result.gpa = 0

            result.subject_assignment_marks = assignment_marks
            result.subject_exam_marks = exam_marks
            result.save()
            messages.success(request, "Result Updated Successfully!")
            return redirect('teacher_add_result')
        else:
            teacher_id_cu = CustomUser.objects.get(id=request.user.id)
            teacher_id = Teachers.objects.get(admin=teacher_id_cu)
            result = StudentResult(student_id=student_obj,teacher_id=teacher_id,exam_id=exam_obj, subject_id=subject_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
            exam_fraction = int(exam_marks) / int(assignment_marks) 
            exam_percentage = int(exam_fraction * 100)
                       
            if exam_percentage >= 80:
                result.gpa = 5.00
            elif exam_percentage >= 70:
                result.gpa = 4.00
            elif exam_percentage >= 60:
                result.gpa = 3.50
            elif exam_percentage >= 50:
                result.gpa = 3.00
            elif exam_percentage >= 40:
                result.gpa = 2.00
            elif exam_percentage >= 33:
                result.gpa = 1.00
            elif exam_percentage < 33 :
                result.gpa = 0

            result.save()
             # try:
            check_total_marks_exist = TotalMarks.objects.filter(student_id=student_obj,exam_id=exam_obj).exists()
            if check_total_marks_exist:
                    totalMarks = TotalMarks.objects.get(exam_id=exam_obj,student_id=student_obj)
                    oldTotalMark = int(totalMarks.total_marks)
                    oldObtainedMark = int(totalMarks.obtained_marks)
                    newObtianedMark = oldObtainedMark + int(exam_marks)
                    newTotalMark = oldTotalMark + int(assignment_marks)
                    totalMarks.total_marks = newTotalMark
                    totalMarks.exam_date = exam_obj.exam_date
                    totalMarks.obtained_marks = newObtianedMark
                    
                    totalMarks.save()
            else:            
                totalMarks = TotalMarks(exam_id=exam_obj,total_marks=assignment_marks,obtained_marks=exam_marks,student_id=student_obj,exam_date=exam_obj.exam_date)
                totalMarks.save()
            messages.success(request, "Result Added Successfully!")
            return redirect('teacher_add_result')
        # except:
        #     messages.error(request, "Failed to Add Result!")
        #     return redirect('teacher_add_result')


def add_online_class(request):
    
    # teacher_obj = CustomUser.objects.get(id=request.user.id)
    pcc = PCC.objects.filter(teacher_id=request.user.id)
    online_classes = OnlineClass.objects.filter(teacher_id=request.user.id)
    classes = Classes.objects.all()
    context = {
        "pcc":pcc ,
        "online_classes" : online_classes ,
        "classes" : classes ,
    }

    return render(request, "teacher_template/add_online_class.html",context)

def get_online_class(request):

    
    class_id = request.POST.get("className")
    batch_id = request.POST.get("batch")
    o_c_name = request.POST.get("online_class_name")
    o_c_link = request.POST.get("online_class_link")

    

    c_id = Classes.objects.get(id=class_id)
    b_id= SectionOrBatch.objects.get(id=batch_id)



    online_class = OnlineClass(online_class_name=o_c_name , online_class_link=o_c_link , class_id=c_id , batch_id=b_id , teacher_id=request.user , status=False)
    online_class.save()
    
     # Only Passing Student Id and Student Name Only
    
    messages.success(request, "Successfully Added Class")
    return redirect('add_online_class')

def play_class(request, class_id):
    online_class = OnlineClass.objects.get(id=class_id)
    online_class.status = True
    online_class.save()
    messages.success(request,"Started the Class...Online Class has been Posted on Student Timeline successfully!")
    return redirect('add_online_class')

def pause_class(request, class_id):
    online_class = OnlineClass.objects.get(id=class_id)
    online_class.status = False
    online_class.save()
    messages.warning(request,"Class Stopped")
    return redirect('add_online_class')

def delete_class(request, class_id):
    online_class = OnlineClass.objects.get(id=class_id)
    online_class.delete()
    messages.error(request,"Class Deleted")
    return redirect('add_online_class')

@csrf_exempt
def get_exams(request):
    # Getting Values from Ajax POST 'Fetch Student'
    student_id = request.POST.get("student_id")
    custUser = CustomUser.objects.get(id=student_id)
    student_obj = Students.objects.get(admin=custUser)
    class_model = student_obj.class_id

    batch_model = student_obj.batch_id



    exams = Examination.objects.filter(class_id=class_model, batch_id=batch_model).order_by("-exam_date")



    

    exam_values = exams.values()

    exam_data = list(exam_values)


    # Only Passing Student Id and Student Name Only
    # list_datas = []

    # for exam in exams:
    #     data_small={"id":exam.id, "examName":exam.exam_name, "examDate":exam.exam_date}
    #     list_datas.append(data_small)

    return JsonResponse({"status":"save" , "exam_data":exam_data})
        
        # json.dumps(list_datas), content_type="application/json", safe=False)


@csrf_exempt
def get_exam_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    coachingID = request.POST.get('coachingID')  
        
    studentCU = CustomUser.objects.get(username=coachingID)
    students = Students.objects.get(admin=studentCU)
    if students.active_status ==True :
        batch = students.batch_id
        teacher_id = CustomUser.objects.get(id=request.user.id)
        pccsubjects = PCC.objects.filter(batch_id=batch,teacher_id=teacher_id)
        
        subjectsJson = []
        for i in pccsubjects:
            subject_name = i.subject_id.subject_name
            id = i.subject_id.id
            subject = {
                "subject_name" : subject_name , 
                "id" : id ,
            }
            subjectsJson.append(subject)
        
        details = []
        data = {
            "name" : studentCU.first_name+" "+studentCU.last_name ,
            "id" : studentCU.id
        }
        details.append(data)
    else:
        details=[{"name":"Student Not Availble" , "id":"None"}]

    return JsonResponse({"status":"save" , "details":details , "subjects" : subjectsJson })
        
        

# @csrf_exempt
# def load_subjects_for_student(request):
    

@csrf_exempt
def check_attendance_exist(request):
    date = request.POST.get("date")
    batch_id = request.POST.get("batch")
    class_id = request.POST.get("class_id")
    batch_obj  = SectionOrBatch.objects.get(id=batch_id)
    class_obj = Classes.objects.get(id=class_id)
    
    attendance_obj = Attendance.objects.filter(attendance_date=date,class_id=class_obj,batch_id=batch_obj).exists()
    if attendance_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
        
        

@csrf_exempt
def check_class_reg_exist(request):
    date = request.POST.get("date")
    pcc_id = request.POST.get("pcc_id")
    
    pcc = PCC.objects.get(id=pcc_id)
    
    # batch_obj  = pcc.batch_id
    # class_obj = pcc.class_id
    # subject_obj = pcc.subject_id
    
    reg_obj = ClassAndPayment.objects.filter(class_date=date , pcc_id=pcc).exists()
    if reg_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
        

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def teacher_download_invoice_view(request,payment_id):
    payments = Payment_Teacher.objects.get(id=payment_id)
    pdfDetails = PDFDetails.objects.all().last()
    now = datetime.now()
    
    mydict={
        'pdfDetails' : pdfDetails ,
        'payment' : payments ,
        'now' : now ,
    }
    
    return render_to_pdf('teacher_template/download_invoice.html',mydict)

def teachers_payment_section(request):
    tcu = CustomUser.objects.get(id=request.user.id)
    teacher_obj = Teachers.objects.get(admin=tcu)
    payments = Payment_Teacher.objects.filter(teacher_id=teacher_obj).order_by("-paying_date")
    reg = ClassAndPayment.objects.filter(teacher_id=teacher_obj , status=1).order_by("-class_date")

    totalPayment = reg.aggregate(Sum('per_class_charge'))
    totalPaymentLists = list(totalPayment.values())[0]
    try:
        totalPaymentList = int(totalPaymentLists)
    except:
        totalPaymentList = 0
    paidPayment = payments.aggregate(Sum('payment_amount'))
    paidPaymentLists = list(paidPayment.values())[0]

    try:
        paidPaymentList = int(paidPaymentLists)
    except:
        paidPaymentList = 0
    duePayment = totalPaymentList - paidPaymentList
    context = {
        'payments' : payments ,
        'reg' : reg ,
        'totalPaymentList' : totalPaymentList ,
        'paidPaymentLists' : paidPaymentLists ,
        'duePayment' : duePayment ,
    }
    return render(request,"teacher_template/teachers_payment_section.html",context)
@csrf_exempt
def get_teacher_payments(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('teachers_payment_section')
    else:
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_parse = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date_parse = datetime.strptime(end_date,"%Y-%m-%d").date()

        tcu = CustomUser.objects.get(id=request.user.id)
        teacher_obj = Teachers.objects.get(admin=tcu)
        payments = Payment_Teacher.objects.filter(teacher_id=teacher_obj , payment_upto__range=(start_date_parse,end_date_parse)).order_by("-paying_date")
        reg = ClassAndPayment.objects.filter(teacher_id=teacher_obj, status=1 , class_date__range=(start_date_parse,end_date_parse)).order_by("-class_date") 
        paymentsVal = payments.values()
        paymentsList = list(paymentsVal)
        regVal = reg.values()
        regList = list(regVal)
        totalPayment = reg.aggregate(Sum('per_class_charge'))
        totalPaymentLists = list(totalPayment.values())[0]
        try:
            totalPaymentList = int(totalPaymentLists)
        except:
            totalPaymentList = 0
        paidPayment = payments.aggregate(Sum('payment_amount'))
        paidPaymentLists = list(paidPayment.values())[0]

        try:
            paidPaymentList = int(paidPaymentLists)
        except:
            paidPaymentList = 0
        duePayment = totalPaymentList - paidPaymentList
        adetails=[]
        for i in reg:
            className = i.pcc_id.class_id.class_name
            batchName = i.pcc_id.batch_id.batch_name
            subjectName = i.pcc_id.subject_id.subject_name
            details = {
                "clss" : className ,
                "batch" : batchName ,
                "subject" : subjectName
            }
            adetails.append(details)

        return JsonResponse({'status':'OK' , 'adetails':adetails , 'payments':paymentsList,'reg':regList,'totalPaymentList':totalPaymentList,'paidPaymentList':paidPaymentList,'duePayment':duePayment})
def manage_assigned_classes(request):
    classes = PCC.objects.filter(teacher_id=request.user.id)
    context = {
        "classes" : classes ,
        }
    return render(request,"teacher_template/manage_assigned_classes.html",context)