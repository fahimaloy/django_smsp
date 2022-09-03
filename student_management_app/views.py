# from channels.auth import login, logout
from django.template import context
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import BlogPost, Classes, Contact, CustomUser, Notifications, SectionOrBatch, Subjects , Students, Teachers
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .serializers import StudentProfilePicSerializer , TeacherProfilePicSerializer
from student_management_app.EmailBackEnd import EmailBackEnd


@csrf_exempt
def dp(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.user_type == "3" or user.user_type == 3:
        student = Students.objects.get(admin = user)
        # print(student.profile_pic)
        serializer = StudentProfilePicSerializer(student)
        return JsonResponse(serializer.data)
    elif user.user_type == "2" or user.user_type == 2:
        teacher = Teachers.objects.get(admin = user)
        # print(Teacher.profile_pic)
        serializer = TeacherProfilePicSerializer(teacher)
        return JsonResponse(serializer.data)

def home(request):
    return render(request, 'index.html')
@csrf_exempt
def load_batch(request):
    if request.method != "POST":
        return HttpResponse("Error")
    else:
        class_id = request.POST.get('classes')
        class_obj = Classes.objects.get(id=class_id)
        batch = SectionOrBatch.objects.filter(class_id=class_obj)
        batchVal = batch.values()
        batchJson = list(batchVal)
        print(batchJson)
        return JsonResponse({'status':'OK','batchJson':batchJson})
@csrf_exempt
def load_subject(request):
    if request.method != "POST":
        return HttpResponse("Error")
    else:
        
        batch_id = request.POST.get('batches')
        
        batch_obj = SectionOrBatch.objects.get(id=batch_id)
        subject = Subjects.objects.filter(batch_id=batch_obj)
        subjectVal = subject.values()
        subjectJson = list(subjectVal)
        print(subjectJson)
        return JsonResponse({'status':'OK','subjectJson':subjectJson})
        

def loginPage(request):
    return render(request, 'login.html')
def about(request):
    return render(request, 'contact.html')
def save_contact(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    message = request.POST.get('message')
    contact = Contact(name=name,phone=phone,message=message)
    notification = Notifications(title="A New Message Arrived from some unknown Gardian",link="/contact_message")
    contact.save()
    notification.save()
    return redirect('login')
def blog(request):
    blogs = BlogPost.objects.all()[:4]
    context = {
        "blog" : blog ,
    }
    return render(request,"blog.html",context)

@csrf_exempt
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                email = request.POST.get('email')
                cu = CustomUser.objects.get(username=email)
                teacher = Teachers.objects.get(admin=cu.id)
                if teacher.active_status == True:

                    return redirect('teacher_home')
                else:
                    messages.error(request, "Your Account has been Disabled by the Administration! Please Contact us for any help!")
                    return redirect('login')                
            elif user_type == '3':
                email = request.POST.get('email')
                cu = CustomUser.objects.get(username=email)
                student = Students.objects.get(admin=cu.id)
                if student.active_status == True:

                    return redirect('student_home')
                else:
                    messages.error(request, "Your Account has been Disabled by the Administration! Please Contact us for any help!")
                    return redirect('login')
            elif user_type == '4':
                # return HttpResponse("Accountant Login")
                return redirect('accountant_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


from django.shortcuts import render

# Create your views here.
