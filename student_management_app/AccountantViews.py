import requests
from datetime import datetime 
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from student_management_app.models import PDFDetails , Accountants, CustomUser,AdditionalExpenses , Notices , Teachers, TotalMarks , Examination , StudentResult , Classes, Subjects, Students, SectionOrBatch, FeedBackStudent, FeedBackTeachers, LeaveReportStudent,  ClassAndPayment, Attendance, AttendanceReport, PaymentStudent ,Payment_Teacher , FeesReport ,PCC





def accountant_home(request):
    return render(request, "accountant_template/accountant_home_template.html")



@csrf_exempt
def get_students_fees(request):
    # Getting Values from Ajax POST 'Fetch Student'
    class_id = request.POST.get("classes")
    batch = request.POST.get("batch")

    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    class_model = Classes.objects.get(id=class_id)

    batch_model = SectionOrBatch.objects.get(id=batch)

    students = Students.objects.filter(class_id=class_model, batch_id=batch_model  , active_status = True)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name, "feesAmount":student.feesAmount }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



def take_fees(request):
    classes = Classes.objects.all()
    batch = SectionOrBatch.objects.all()
    taken_fees = FeesReport.objects.all().order_by('-created_at')
    context = {
        "taken_fees" : taken_fees ,
        "classes": classes,
        "batches": batch
    }
    return render(request, "accountant_template/accountant_take_fees_template.html", context)




@csrf_exempt
def save_fees_data(request):

    students_ids = request.POST.get("students_ids")
    class_id = request.POST.get("class_id")

    fees_title = request.POST.get("fees_title")
    additional_fees_title = request.POST.get("additional_title")
    fees_month = request.POST.get("fees_date")
    additional_amount = request.POST.get("additional_amount")
    batch_id = request.POST.get("batch_id")

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
                fees_report = FeesReport(student_id=student,class_id=class_model, fees_date=fees_date,fees_title=fees_title,batch_id=batch_model,amount=student.feesAmount,extra_fees_title=additional_fees_title,extra_amount=additional_amount,paid_status=0,action=0,status=stud['status'])
                phoneNumber = "88"+str(student.smsMobile)
                # message_body = "সম্মানিত অভিভাবক, আগামী ১০ তারিখের মধ্যে "+ fees_title +" সংশ্লিষ্ট "+ str(student.feesAmount) +" টাকা পরিশোধ করার জন্য বিশেষ ভাবে অনুরোধ করা হলো ।  ধন্যবাদান্তে , Alim's Academy "
                message_body = "সম্মানিত অভিভাবক, আগামী ১০ তারিখের মধ্যে শিক্ষার্থীঃ "+ str(student.admin.first_name)+" "+str(student.admin.last_name)+"("+str(student.admin.username)+") এর "+fees_title +" সংশ্লিষ্ট "+ str(student.feesAmount) +" টাকা পরিশোধ করার জন্য বিশেষ ভাবে অনুরোধ করা হলো ।  ধন্যবাদান্তে , Alim's Academy "
                url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

                payload  = {}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data = payload)

                # print(response.text.encode('utf8'))
                # print(url)
                fees_report.save()
            elif stat == 0:
                pass
        
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")





def update_fees(request):
    classes = Classes.objects.all()
    batch = SectionOrBatch.objects.all()
    context = {
        "classes": classes,
        "batch": batch
    }
    return render(request, "accountant_template/update_fees_template.html", context)


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







def accountant_teacher_payment_date_filter(request):

    teachers = Teachers.objects.all() # Getting the Subjects of class Enrolled
    context = {
        "teachers": teachers
    }
    return render(request, "accountant_template/accountant_teacher_payment_date_filter.html", context)


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
# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
def accountant_download_invoice_view(request,payment_id):
    # order=models.Orders.objects.get(id=orderID)
    # product=models.Product.objects.get(id=productID)
    paymentStudent = FeesReport.objects.get(id=payment_id)
    
    now = datetime.now()
    
    mydict={
        
        'paymentStudent' : paymentStudent ,
        'now' : now ,
    }
    
    return render_to_pdf('admin_template/download_invoice.html',mydict)

@csrf_exempt
def accountant_teacher_payment_date_filter_single(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('accountant_teacher_payment_date_filter')
    else:
        # try:
        
        teacher_id = request.POST.get("teachers")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        
        start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()

        



        # try:
        payment_details = Payment_Teacher.objects.filter(teacher_id=teacher_id , payment_upto__range=(start_date_parse, end_date_parse))

        payment_details_values = payment_details.values()

        payment_data = list(payment_details_values)


        teacher_obj = Teachers.objects.get(id=teacher_id)
    
        approved_class = ClassAndPayment.objects.filter(teacher_id=teacher_obj ,class_date__range=(start_date_parse, end_date_parse) , status=1)

        approved_class_values = approved_class.values()

        approved_class_data = list(approved_class_values)
        classes = []
        for i in approved_class:
            clss = i.pcc_id.class_id.class_name
            classes.append(clss)
        total_payment_dict = approved_class.aggregate(Sum('per_class_charge'))

        total_payment_list_values = list(total_payment_dict.values())[0]
            
        paid_payment_dict = payment_details.aggregate(Sum('payment_amount'))
        paid_payment_list_values = list(paid_payment_dict.values())[0]
        try:
            total_payment_list_value = int(total_payment_list_values)
        except:
            total_payment_list_value = 0
        try:
            paid_payment_list_value = int(paid_payment_list_values)
        except:
            paid_payment_list_value = 0
            

        due_payment = total_payment_list_value - paid_payment_list_value

        return JsonResponse({'status':'Save','classes':classes ,'payment_data' : payment_data,'approved_class_data':approved_class_data , 'total_payment_list_value':total_payment_list_value,'paid_payment_list_value':paid_payment_list_value,'due_payment':due_payment})

        #     except:
        #         return JsonResponse({'status':'None'})

        # except:
        #     messages.error(request, "Failed to Fetch Details . Check dates Correctly!!")
        #     return redirect('accountant_teacher_payment_date_filter')


@csrf_exempt
def accountant_add_teachers_payment(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect(reverse('accountant_teacher_payment_date_filter'))
    else:
        try:
            teacher_id = request.POST.get('teachers')
            pay_upto  = request.POST.get('paymentUpto')
            payment_amount = request.POST.get('paymentAmount')

            teacher_obj = Teachers.objects.get(id=teacher_id)
            # try:
            leave_report = Payment_Teacher(teacher_id=teacher_obj,payment_upto=pay_upto, payment_amount=payment_amount )
            phoneNumber = "88"+str(teacher_obj.mobileNumber)
            message_body = "Dear "+teacher_obj.admin.first_name+" "+teacher_obj.admin.last_name+" Sir,  "+payment_amount +" ৳ honorium has been paid as your contribution to the institute upto "+str(pay_upto)+" . We appreciate your cooperation. Best Regards! Alim's Academy"
            url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

            payload  = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", url, headers=headers, data = payload)

            print(response.text.encode('utf8'))
            print(url)
            leave_report.save()
            return HttpResponse("True")

        except:
            return HttpResponse("False")


def accountant_student_apply_payment(request):
    students = Students.objects.all()
    classes = Classes.objects.all()
    batches = SectionOrBatch.objects.all()
    payment_details = FeesReport.objects.filter(paid_status=1).order_by("-paid_at")
    context = {
        "students": students ,
        "classes": classes ,
        "batches": batches ,
        "payment_details" : payment_details ,
    }
    return render(request, 'accountant_template/accountant_student_apply_payment.html', context)


@csrf_exempt
def accountant_student_apply_payment_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('accountant_student_apply_payment')
    else:
        
        payment_id = request.POST.get('payment_id')
        bkash_nmb = request.POST.get('bkash_nmb')
        trans_id = request.POST.get('trans_id')
        in_cash = request.POST.get('in_cash')
        

        
        try:
            fees = FeesReport.objects.get(id=payment_id)
            fees.action = 1
            fees.in_cash = in_cash
            fees.bkash_nmb = bkash_nmb
            fees.trans_id = trans_id
            fees.paid_at = datetime.now()
            fees.paid_status = 1
            phoneNumber = "88"+str(fees.student_id.smsMobile)
            # message_body = "Congratulations! "+str(fees.amount)+"Taka , For "+ str(fees.fees_title) +" has been recieved. Have a Great Day! Alim's Academy"
            message_body = "অভিনন্দন! নামঃ "+str(fees.student_id.admin.first_name)+" "+str(fees.student_id.admin.last_name)+"("+str(fees.student_id.admin.username)+ ") শ্রেনিঃ "+str(fees.student_id.class_id.class_name)+"("+ str(fees.student_id.batch_id.batch_name) +") "+ str(fees.fees_title) +" বাবদ "+str(fees.amount)+"টাকা পরিশোধ করা হয়েছে । ধন্যবাদান্তে আলিম'স একাডেমি " 
            url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

            payload  = {}
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data = payload)

            print(response.text.encode('utf8'))
            print(url)
            fees.save()
            return HttpResponse("True")

        except:
            return HttpResponse("False")


@csrf_exempt
def accountant_get_student_payment(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('accountant_student_apply_payment')
    else:
        coachingIDsearch = request.POST.get('coachingIDsearch')
        # start_date = request.POST.get("start_date")
        # end_date = request.POST.get("end_date")
        # start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        student_id = CustomUser.objects.get(username=coachingIDsearch)
        student_obj = Students.objects.get(admin=student_id.id)
        payment_student = FeesReport.objects.filter(student_id=student_obj,paid_status=1)
        
        admin = CustomUser.objects.filter(username=coachingIDsearch).values()
        adminList = list(admin)
            
        fees = FeesReport.objects.filter(student_id=student_obj).order_by("paid_status")
        fees_values = fees.values()
        fees_details = list(fees_values)

        totalFees = fees.aggregate(Sum('amount'))
        totalFeesLists = list(totalFees.values())[0]


        totalPaid = payment_student.aggregate(Sum('amount'))
        totalPaidLists = list(totalPaid.values())[0]
        
        try:
            totalPaidList = int(totalPaidLists)
        except:
            totalPaidList = 0
        try:
            totalFeesList = int(totalFeesLists)
        except:
            totalFeesList = 0
    
        totalDue =  totalFeesList - totalPaidList
    
    
        return JsonResponse({'status':'Done', 'adminList':adminList ,'fees_details' : fees_details , 'totalFeesList':totalFeesList , 'totalPaidList':totalPaidList , 'totalDue':totalDue})
        # 'fees_details':fees_details
        


        


@csrf_exempt
def accountant_add_student_payment(request,payment_id):
    payment = FeesReport.objects.get(id=payment_id)
    context = {
        'payment':payment
    }
    return render(request,"accountant_template/make_payment.html",context)
def accountant_add_student_payment_save(request):
    try:
        student_id = request.POST.get('student_id')
        pay_upto  = request.POST.get('pay_upto')
        amount = request.POST.get('amount')
        in_cash = request.POST.get('in_cash')
        bkash_nmb = request.POST.get('bkash_nmb')
        trans_id = request.POST.get('trans_id')
        class_id = request.POST.get('class_id')
        batch_id = request.POST.get('batch')


        student_obj = Students.objects.get(admin=student_id)
        class_obj = Classes.objects.get(id=class_id)
        batch_obj = SectionOrBatch.objects.get(id=batch_id)

        payment = PaymentStudent(student_id=student_obj,class_id=class_obj,batch_id=batch_obj,pay_upto=pay_upto,amount=amount,payment_status=1,in_cash=in_cash,bkash_nmb=bkash_nmb,trans_id=trans_id)
        
        phoneNumber = "88"+str(student_obj.smsMobile)
        message_body = "Greetings from Alim's Academy!  "+str(amount)+"Taka , Upto "+ str(pay_upto) +" has been recieved. Have a Great Day!"
        url = "http://66.45.237.70/api.php?username=aalim7374&password=ZNCS4AB9&number="+ phoneNumber +"&message="+ message_body +""

        payload  = {}
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))
        print(url)
        payment.save()

                
        return HttpResponse("True")

    except:
        return HttpResponse("False")

def accountant_expenses(request):
    paymentTeacher = Payment_Teacher.objects.all().order_by("-payment_upto")
    paymentStudent = FeesReport.objects.filter(paid_status=1).order_by("-paid_at")
    additionalExpenses = AdditionalExpenses.objects.all().order_by("-date")
    # totalpaid = Payment_Teacher.objectts.
    totalpaid = paymentTeacher.aggregate(Sum('payment_amount'))
    totalpaidlists = list(totalpaid.values())[0]

    totalobtained = paymentStudent.aggregate(Sum('amount'))
    totalobtainedlists = list(totalobtained.values())[0]
    
    totalAE = additionalExpenses.aggregate(Sum('amount'))
    totalAElists = list(totalAE.values())[0]
    
    try:
        totalpaidlist = int(totalpaidlists)
        
    except:
        totalpaidlist = 0
     
    try:
        totalobtainedlist = int(totalobtainedlists)
        
    except:
        totalobtainedlist = 0
        
    try:
        totalAElist = int(totalAElists)
        
    except:
        totalAElist = 0
         
    totalexpenses = totalpaidlist + totalAElist
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
    }
    return render(request,"accountant_template/expenses.html",context)

@csrf_exempt
def accountant_add_expenses(request):
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
def accountant_get_expenses(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    
    start_date_parse = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    paymentTeacher = Payment_Teacher.objects.filter(payment_upto__range=(start_date_parse , end_date_parse)).order_by("-payment_upto")
    paymentTeacherValues = paymentTeacher.values()
    paymentTeacherList = list(paymentTeacherValues)

    paymentStudent = FeesReport.objects.filter(paid_status=1,pay_upto__range=(start_date_parse , end_date_parse)).order_by("-paid_at")

    paymentStudentValues = paymentStudent.values()

    paymentStudentList = list(paymentStudentValues)

    additionalExpenses = AdditionalExpenses.objects.filter(date__range=(start_date_parse , end_date_parse))
  

    
    pt = Payment_Teacher.objects.filter(payment_upto__range=(start_date_parse , end_date_parse))
    ptList = []
    for i in pt:
        teacher_name = Teachers.objects.get(id=i.teacher_id.id)
        ptList.append(teacher_name.admin.first_name+" "+teacher_name.admin.last_name)
    
    st = PaymentStudent.objects.filter(pay_upto__range=(start_date_parse , end_date_parse))
    stList = []
    for i in st:
        student_name = Students.objects.get(id=i.student_id.id)
        stList.append(student_name.admin.first_name+" "+student_name.admin.last_name)
    expenses = AdditionalExpenses.objects.filter(date__range=(start_date_parse , end_date_parse))
    expensesValues = expenses.values()
    expensesList = list(expensesValues)
    
    totalpaid = paymentTeacher.aggregate(Sum('payment_amount'))
    totalpaidlists = list(totalpaid.values())[0]

    totalobtained = paymentStudent.aggregate(Sum('amount'))
    totalobtainedlists = list(totalobtained.values())[0]
    
    totalAE = additionalExpenses.aggregate(Sum('amount'))
    totalAElists = list(totalAE.values())[0]
    
    try:
        totalpaidlist = int(totalpaidlists)
        
    except:
        totalpaidlist = 0
     
    try:
        totalobtainedlist = int(totalobtainedlists)
        
    except:
        totalobtainedlist = 0
        
    try:
        totalAElist = int(totalAElists)
        
    except:
        totalAElist = 0
         
    totalexpenses = totalpaidlist + totalAElist
    totalprofit = totalobtainedlist - totalexpenses
    return JsonResponse({'status':'OK', 'ptList':ptList , 'totalprofit':totalprofit ,'totalobtainedlist':totalobtainedlist , 'totalexpenses':totalexpenses , 'totalAElist':totalAElist , 'totalpaidlist':totalpaidlist, 'stList':stList ,'expensesList':expensesList,'paymentStudentList':paymentStudentList ,'paymentTeacherList':paymentTeacherList})
    


    


