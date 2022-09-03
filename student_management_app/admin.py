from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BlogPost, CustomUser, Admin, Notifications,PaymentStudent , PDFDetails , SectionOrBatch , AdditionalExpenses , FeesReport , Teachers, Classes,Subjects, TotalMarks,Students, Attendance, AttendanceReport, LeaveReportStudent,  FeedBackStudent, FeedBackTeachers,  FeesReport , PCC , ClassAndPayment , Payment_Teacher , StudentResult , Examination , OnlineClass

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
admin.site.register(Notifications)
admin.site.register(Admin)
admin.site.register(OnlineClass)
admin.site.register(Teachers)
admin.site.register(Classes)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(Payment_Teacher)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackTeachers)
admin.site.register(StudentResult)
admin.site.register(Examination)
admin.site.register(TotalMarks)
admin.site.register(FeesReport)
admin.site.register(PCC)
admin.site.register(ClassAndPayment)
admin.site.register(PaymentStudent)
admin.site.register(AdditionalExpenses)
admin.site.register(PDFDetails)
admin.site.register(BlogPost)
admin.site.register(SectionOrBatch)





# NotificationStudent, NotificationStaffs , 