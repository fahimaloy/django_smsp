import requests
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
# import datetime # To Parse input DateTime into Python Date Time Object

from student_management_app.models import CustomUser, FeesReport, Notices ,Examination, Notifications, OnlineClass, SectionOrBatch ,Teachers, Classes, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult, PaymentStudent , TotalMarks


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    class_obj = Classes.objects.get(id=student_obj.class_id.id)
    total_subjects = Subjects.objects.filter(class_id=class_obj).count()

    totalPaidPaymentFilter = FeesReport.objects.filter(student_id=student_obj,paid_status=1)
    totalPaidPaymentAmount = totalPaidPaymentFilter.aggregate(Sum('amount'))
    totalPaidPayments = list(totalPaidPaymentAmount.values())[0]
    


    feesFilter = FeesReport.objects.filter(student_id=student_obj)
    totalFeesAmount = feesFilter.aggregate(Sum('amount'))
    totalFee = list(totalFeesAmount.values())[0]
    
    try:
        totalPaidPayment = int(totalPaidPayments)
    except:
        totalPaidPayment = 0
    try:
        totalFees = int(totalFee)
    except:
        totalFees = 0

    totalDue = totalFees - totalPaidPayment
    
    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(class_id=student_obj.class_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter()
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": totalDue,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id) # Getting Logged in Student Data
    classes = student.class_id # Getting class Enrolled of LoggedIn Student
    # class = Classes.objects.get(id=student.class_id.id) # Getting class Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(class_id=classes) # Getting the Subjects of class Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse))
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)

##########
##########


def student_apply_payment(request):
    student_obj = Students.objects.get(admin=request.user.id)
    payment_data = FeesReport.objects.filter(student_id=student_obj).order_by('-fees_date')
    totalPaidPaymentFilter = FeesReport.objects.filter(student_id=student_obj,paid_status=1)
    totalPaidPaymentAmount = totalPaidPaymentFilter.aggregate(Sum('amount'))
    totalPaidPayment = list(totalPaidPaymentAmount.values())[0]
    

    

    feesFilter = FeesReport.objects.filter(student_id=student_obj)
    totalFeesAmount = feesFilter.aggregate(Sum('amount'))
    totalFees = list(totalFeesAmount.values())[0]
    
    try:
        totalDue = totalFees - totalPaidPayment
    except:
        totalDue = 0
    student_obj = Students.objects.get(admin=request.user.id)
    class_id = Classes.objects.get(id=student_obj.class_id.id)
    batch_id = SectionOrBatch.objects.get(id=student_obj.batch_id.id)
    
    context = {
        "class_id": class_id ,
        "batch_id": batch_id ,
        "payment_data": payment_data ,
        "totalPaidPayment" : totalPaidPayment ,
        "totalFees" : totalFees ,
        "totalDue" : totalDue ,
        "student_obj":student_obj ,
        
    }
    return render(request, 'student_template/payment_apply.html', context)


@csrf_exempt
def student_apply_payment_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_payment')
    else:
        
        payment_id = request.POST.get('payment_id')
        bkash_nmb = request.POST.get('bkash_nmb')
        trans_id = request.POST.get('trans_id')
        in_cash = request.POST.get('in_cash')
        

        
        try:
            fees = FeesReport.objects.get(id=payment_id)
            fees.action = 3
            fees.in_cash = in_cash
            fees.bkash_nmb = bkash_nmb
            fees.trans_id = trans_id
            fees.save()
            notifications=Notifications(title="A Fees hasbeen applied by a student"+ fees.student_id.admin.first_name +" "+fees.student_id.admin.last_name,link="")
            return HttpResponse("True")

        except:
            return HttpResponse("False")

def make_payment(request,payment_id):
    payment = FeesReport.objects.get(id=payment_id)
    context = {
        'payment':payment ,
    }
    return render(request,"student_template/make_payment.html",context)
##########
##########


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            notifications = Notifications(title="A Student has Submitted a Report",link="/student_feedback_message/"+add_feedback.id+"/")
            notifications.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        # address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
                student = Students.objects.get(admin=customuser)
                phoneNumber = "88"+student.mobile +",88"+student.fathersMobile+",88"+student.mothersMobile
                message_body = "Congratulations "+ customuser.first_name +" "+ customuser.last_name +"!Your Password Have been Changed. Your New Login Details are given below : CoachingID: "+ customuser.username +" Password: "+ password+" . Best Regards Alim's Academy"
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""
    
                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
                response = requests.request("POST", url, headers=headers, data = payload)

            customuser.save()

            
            messages.success(request, "Profile Updated Successfully")
            return redirect('login')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')
from django.db.models import Sum



def online_class(request):
    student_obj = Students.objects.get(admin=request.user.id)

    online_class = OnlineClass.objects.filter(class_id=student_obj.class_id ,batch_id=student_obj.batch_id , status=True)

    context = {
        "online_class" : online_class ,
    }

    return render(request,"student_template/online_class.html",context)


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id).order_by("-exam_id")
    
    examinations = Examination.objects.filter(status=1 , class_id=student.class_id , batch_id = student.batch_id).order_by("-exam_date")
    # filter(status=1, batch_id=student.batch_id.id ).order_by("-exam_date")
    totalMarks = TotalMarks.objects.filter(student_id=student.id,status=1)

    totalWorkingDay = AttendanceReport.objects.filter(student_id=student.id).count()
    totalPresent = AttendanceReport.objects.filter(student_id=student.id , status=True).count()
    totalAbsent = AttendanceReport.objects.filter(student_id=student.id , status=False).count()

        
    totalMarksDict = totalMarks.aggregate(Sum('total_marks'))

    totalMarksVal = list(totalMarksDict.values())[0]


    obtainedMarksDict = totalMarks.aggregate(Sum('obtained_marks'))

    obtainedMarksVal = list(obtainedMarksDict.values())[0]


    
    context = {
        "totalMarks" : totalMarks ,
        "totalMarksVal":totalMarksVal,
        "obtainedMarksVal" : obtainedMarksVal ,
        "totalWorkingDay" : totalWorkingDay ,
        "totalPresent" : totalPresent ,
        "totalAbsent" : totalAbsent ,
        "student_result": student_result,
        "examinations" : examinations ,
    }
    return render(request, "student_template/student_view_result.html", context)





from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_student_report_card(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_result')
    else:
        # try:
        # pass
        


            
        student = Students.objects.get(admin=request.user.id)
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

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

def view_notices(request):
    student_obj = Students.objects.get(admin=request.user.id)
    class_obj = Classes.objects.get(id=student_obj.class_id.id)
    batch_obj = SectionOrBatch.objects.get(id=student_obj.batch_id.id)

    notices = Notices.objects.filter(class_id=class_obj,batch_id=batch_obj)

    context = {
        'notices' : notices ,
    }
    return render(request,"student_template/view_notices.html",context)

@csrf_exempt
def student_get_payment_date(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    student_obj = Students.objects.get(admin=request.user.id)
    
    payments = FeesReport.objects.filter(student_id=student_obj , fees_date__range=(start_date_parse,end_date_parse)).order_by('-fees_date')
    paymentsvalues = payments.values()
    paymentslist = list(paymentsvalues)
    
    
    totalPaidPaymentFilter = FeesReport.objects.filter(student_id=student_obj,paid_status=1,fees_date__range=(start_date_parse,end_date_parse))
    totalPaidPaymentAmount = totalPaidPaymentFilter.aggregate(Sum('amount'))
    totalPaidPayments = list(totalPaidPaymentAmount.values())[0]
    


    feesFilter = FeesReport.objects.filter(student_id=student_obj,fees_date__range=(start_date_parse,end_date_parse))
    totalFeesAmount = feesFilter.aggregate(Sum('amount'))
    totalFee = list(totalFeesAmount.values())[0]
    
    try:
        totalPaidPayment = int(totalPaidPayments)
    except:
        totalPaidPayment = 0
    try:
        totalFees = int(totalFee)
    except:
        totalFees = 0
    totalDue = totalFees - totalPaidPayment
    
    return JsonResponse({'status':'OK','payments':paymentslist , 'totalDue':totalDue , 'totalFees' : totalFees , 'totalPaidPayment':totalPaidPayment })



