
from student_management_app import AccountantViews
from django.urls import path, include
from . import views
from .import  StudentViews , AdminViews ,TeacherViews

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('load_batch/', views.load_batch, name='load_batch'),
    path('load_subject/', views.load_subject, name='load_subject'),
    path('about/', views.about, name='about'),
    path('save_contact/', views.save_contact, name='save_contact'),
    path('dp/',views.dp , name='dp'),

    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    
    path('get_students_for_payment', AdminViews.get_students_for_payment , name="get_students_for_payment"),
    path('teacher_payment_date_all/', AdminViews.teacher_payment_date_all, name="teacher_payment_date_all" ),
    path('teacher_payment/', AdminViews.TeacherPayment, name="teacher_payment" ),
    path('delete_payment/<payment_id>/', AdminViews.delete_payment, name="delete_payment" ),
    path('delete_expenses/<expense_id>/', AdminViews.delete_expenses, name="delete_expenses" ),
    path('exam_single/<exam_id>/', AdminViews.exam_single, name="exam_single" ),
    path('delete_single_result/<result_id>/', AdminViews.delete_single_result, name="delete_single_result" ),
    # path('create_blog_post/', AdminViews.create_blog_post, name="create_blog_post" ),
    # path('create_blog_post_save/', AdminViews.create_blog_post_save, name="create_blog_post_save" ),
    path('student_payment/', AdminViews.StudentPayment, name="student_payment" ),
    path('student_payment_single/', AdminViews.StudentPaymentSingle, name="student_payment_single" ),
    path('get_unpaid_payments/', AdminViews.get_unpaid_payments, name="get_unpaid_payments" ),
    path('add_teachers_payment/', AdminViews.add_teachers_payment, name="add_teachers_payment" ),
    path('get_student_by_coaching_id/', AdminViews.get_student_by_coaching_id, name="get_student_by_coaching_id" ),
    path('student_unpaid_date_filter/', AdminViews.student_unpaid_date_filter, name="student_unpaid_date_filter" ),
    path('admin_view_online_class/', AdminViews.admin_view_online_class, name="admin_view_online_class"),
    path('deactivate_student/<student_id>/', AdminViews.deactivate_student, name="deactivate_student"),
    path('re_activate_student/<student_id>/', AdminViews.re_activate_student, name="re_activate_student" ),
    path('deactivate_teacher/<teacher_id>/', AdminViews.deactivate_teacher, name="deactivate_teacher"),
    path('re_activate_teacher/<teacher_id>/', AdminViews.re_activate_teacher, name="re_activate_teacher" ),
    path('load_fees/', AdminViews.load_fees, name="load_fees"),
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    path('add_teacher/', AdminViews.add_teacher, name="add_teacher"),
    path('add_teacher_save/', AdminViews.add_teacher_save, name="add_teacher_save"),
    path('manage_teacher/', AdminViews.manage_teacher, name="manage_teacher"),
    path('manage_fees/', AdminViews.manage_fees, name="manage_fees"),
    path('delete_fees/', AdminViews.delete_fees, name="delete_fees"),
    path('edit_teacher/<teacher_id>/', AdminViews.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save/', AdminViews.edit_teacher_save, name="edit_teacher_save"),
    path('delete_teacher/<teacher_id>/', AdminViews.delete_teacher, name="delete_teacher"),
    path('student_payment_batch_date_filter/', AdminViews.student_payment_batch_date_filter, name="student_payment_batch_date_filter"),
    path('add_accountant/', AdminViews.add_accountant, name="add_accountant"),
    path('add_accountant_save/', AdminViews.add_accountant_save, name="add_accountant_save"),
    path('manage_accountant/', AdminViews.manage_accountant, name="manage_accountant"),
    path('edit_accountant/<accountant_id>/', AdminViews.edit_accountant, name="edit_accountant"),
    path('edit_accountant_save/', AdminViews.edit_accountant_save, name="edit_accountant_save"),
    path('delete_accountant/<accountant_id>/', AdminViews.delete_accountant, name="delete_accountant"),
    path('manage_accountant_single/<accountant_id>/', AdminViews.manage_accountant_single, name="manage_accountant_single"),
    path('delete_student_payment_single/<payment_id>/', AdminViews.delete_student_payment_single, name="delete_student_payment_single"),
    path('seen_notification/<id>/', AdminViews.seen_notification , name="seen_notification"),  # type: ignore
    path('seen_all_notifications/', AdminViews.seen_all_notifications , name="seen_all_notifications"),  # type: ignore
    path('get_admin_view_online_class/', AdminViews.get_admin_view_online_class, name="get_admin_view_online_class"),
    path('add_class/', AdminViews.add_class, name="add_class"),
    path('manage_attendance/', AdminViews.manage_attendance, name="manage_attendance"),
    path('delete_attendance/<attendance_id>/', AdminViews.delete_attendance, name="delete_attendance"),
    path('delete_student_payment/<payment_id>/', AdminViews.delete_student_payment, name="delete_student_payment"),
    path('delete_teacher_payment/<payment_id>/', AdminViews.delete_teacher_payment, name="delete_teacher_payment"),
    path('delete_registered_class/<reg_id>/', AdminViews.delete_registered_class, name="delete_registered_class"),
    path('add_class_save/', AdminViews.add_class_save, name="add_class_save"),
    path('manage_class/', AdminViews.manage_class, name="manage_class"),
    path('edit_class/<class_id>/', AdminViews.edit_class, name="edit_class"),
    path('edit_class_save/', AdminViews.edit_class_save, name="edit_class_save"),
    path('delete_class/<class_id>/', AdminViews.delete_class, name="delete_class"),
    path('manage_batch/', AdminViews.manage_batch, name="manage_batch"),
    path('add_batch/', AdminViews.add_batch, name="add_batch"),
    path('add_batch_save/', AdminViews.add_batch_save, name="add_batch_save"),
    path('edit_batch/<batch_id>', AdminViews.edit_batch, name="edit_batch"),
    path('edit_batch_save/', AdminViews.edit_batch_save, name="edit_batch_save"),
    path('delete_batch/<batch_id>/', AdminViews.delete_batch, name="delete_batch"),
    path('add_student/', AdminViews.add_student, name="add_student"),
    path('add_student_save/', AdminViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', AdminViews.edit_student, name="edit_student"),
    path('edit_student_save/', AdminViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', AdminViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', AdminViews.delete_student, name="delete_student"),
    path('add_subject/', AdminViews.add_subject, name="add_subject"),
    path('add_subject_save/', AdminViews.add_subject_save, name="add_subject_save"),
    path('manage_subject/', AdminViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', AdminViews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', AdminViews.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', AdminViews.delete_subject, name="delete_subject"),
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),
    path('check_roll_exist/', AdminViews.check_roll_exist, name="check_roll_exist"),
    path('student_feedback_message/', AdminViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', AdminViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('teacher_feedback_message/', AdminViews.teacher_feedback_message, name="teacher_feedback_message"),
    path('teacher_feedback_message_reply/', AdminViews.teacher_feedback_message_reply, name="teacher_feedback_message_reply"),
    path('student_leave_view/', AdminViews.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', AdminViews.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', AdminViews.student_leave_reject, name="student_leave_reject"),
    ###
    path('student_payment_view/', AdminViews.student_payment_view, name="student_payment_view"),
    path('student_payment_approve/<payment_id>/', AdminViews.student_payment_approve, name="student_payment_approve"),
    path('student_payment_reject/<payment_id>/', AdminViews.student_payment_reject, name="student_payment_reject"),
    path('assign_subjects_to_teacher/', AdminViews.assign_subjects_to_teacher, name="assign_subjects_to_teacher"),
    path('assign_subjects_to_teacher_save/', AdminViews.assign_subjects_to_teacher_save, name="assign_subjects_to_teacher_save"),
    path('edit_assigned_subjects_to_teacher/<pcc_id>/', AdminViews.edit_assigned_subjects_to_teacher, name="edit_assigned_subjects_to_teacher"),
    path('delete_assigned_subjects_to_teacher/<pcc_id>/', AdminViews.delete_assigned_subjects_to_teacher, name="delete_assigned_subjects_to_teacher"),
    path('edit_assigned_subjects_to_teacher_save/', AdminViews.edit_assigned_subjects_to_teacher_save, name="edit_assigned_subjects_to_teacher_save"),
    path('get_student_batch_search/', AdminViews.get_student_batch_search, name="get_student_batch_search"),
    path('student_payment_batch_filter/', AdminViews.student_payment_batch_filter, name="student_payment_batch_filter"),
    path('get_filter_payment_all/', AdminViews.get_filter_payment_all, name="get_filter_payment_all"),
    path('download-invoice/<payment_id>/', AdminViews.download_invoice_view,name='download-invoice'),
    



    


    path('get_students_fees/', AdminViews.get_students_fees, name="get_students_fees"),
    path('take_fees/', AdminViews.take_fees, name="take_fees"),
    path('save_fees_data/', AdminViews.save_fees_data, name="save_fees_data"),
    path('get_fees_dates/', AdminViews.get_fees_dates, name="get_fees_dates"),
    path('update_fees/', AdminViews.update_fees, name="teacher_update_fees"),  
    path('get_fees_student/', AdminViews.get_fees_student, name="get_fees_student"),
    path('update_fees_data/', AdminViews.update_fees_data, name="update_fees_data"),
    path('single-notice/<notice_id>/', AdminViews.single_notice, name="single-notice"),
    path('single_student_feedback/<feedback_id>/', AdminViews.single_student_feedback, name="single_student_feedback"),
    path('single_teacher_feedback/<feedback_id>/', AdminViews.single_teacher_feedback, name="single_teacher_feedback"),
    path('single_leave/<leave_id>/', AdminViews.single_leave, name="single_leave"),
    path('sms/', AdminViews.sms, name="sms"),
    path('sms_save/', AdminViews.sms_save, name="sms_save"),
    path('get_not_number/', AdminViews.get_not_number, name="get_not_number"),
    path('notiofications/', AdminViews.notiofications, name="notiofications"),
    
    

    

    ###
    path('teacher_class_reg/', AdminViews.teacher_class_reg, name="teacher_class_reg"),
    path('teacher_class_reg_approve/<reg_id>/', AdminViews.teacher_class_reg_approve, name="teacher_class_reg_approve"),
    path('teacher_class_reg_reject/<reg_id>/', AdminViews.teacher_class_reg_reject, name="teacher_class_reg_reject"),
    path('admin_view_attendance/', AdminViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', AdminViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', AdminViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),

    path('teacher_payment_date_filter/', AdminViews.teacher_payment_date_filter, name="teacher_payment_date_filter"),
    path('teacher_payment_all/', AdminViews.teacher_payment_all, name="teacher_payment_all"),
    path('teacher_payment_date_filter_single/', AdminViews.teacher_payment_date_filter_single, name="teacher_payment_date_filter_single"),
    path('manage_teacher_single/<teacher_id>/', AdminViews.manage_teacher_single, name="manage_teacher_single"),
    path('manage_student_single/<student_id>/', AdminViews.manage_student_single, name="manage_student_single"),
    path('view_result/', AdminViews.view_result , name="view_result"),
    path('get_student_report/', AdminViews.get_student_report , name="get_student_report"),
    path('get_student_search/', AdminViews.get_student_search, name="get_student_search"),
    path('expenses/', AdminViews.expenses, name="expenses"),
    path('get_expenses/', AdminViews.get_expenses, name="get_expenses"),
    path('add_expenses/', AdminViews.add_expenses, name="add_expenses"),

    path('add_notice/', AdminViews.add_notice, name="add_notice"),
    path('save_notice/', AdminViews.save_notice, name="save_notice"),
    path('edit_notice/<notice_id>/', AdminViews.edit_notice, name="edit_notice"),
    path('edit_notice_save/', AdminViews.edit_notice_save, name="edit_notice_save"),
    path('delete_notice/<notice_id>/', AdminViews.delete_notice, name="delete_notice"),

    path('add_exam/', AdminViews.add_exam, name="add_exam"),
    path('save_exam/', AdminViews.save_exam, name="save_exam"),
    path('edit_exam_save/', AdminViews.edit_exam_save, name="edit_exam_save"),
    path('edit_exam/<exam_id>/', AdminViews.edit_exam, name="edit_exam"),
    path('delete_exam/<exam_id>/', AdminViews.delete_exam, name="delete_exam"),
    path('publish_result/<exam_id>/', AdminViews.publish_result, name="publish_result"),
    path('download_teacher_invoice_view/<payment_id>/', AdminViews.download_teacher_invoice_view, name="download_teacher_invoice_view"),
    path('download_student_report_card/', AdminViews.download_student_report_card , name="download_student_report_card"),
    path('ask_for_payment/<student_id>/<due>/', AdminViews.ask_for_payment, name="ask_for_payment"),
    
    # URLS for teacher
    path('get_teacher_payments/', TeacherViews.get_teacher_payments, name="get_teacher_payments"),
    path('teachers_payment_section/', TeacherViews.teachers_payment_section, name="teachers_payment_section"),
    path('teacher_download_invoice_view/<payment_id>/', TeacherViews.teacher_download_invoice_view, name="teacher_download_invoice_view"),
    path('teacher_home/', TeacherViews.teacher_home, name="teacher_home"),
    path('teacher_take_attendance/', TeacherViews.teacher_take_attendance, name="teacher_take_attendance"),
    path('get_students/', TeacherViews.get_students, name="get_students"),
    path('save_attendance_data/', TeacherViews.save_attendance_data, name="save_attendance_data"),
    path('teacher_update_attendance/', TeacherViews.teacher_update_attendance, name="teacher_update_attendance"),
    path('get_attendance_dates/', TeacherViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', TeacherViews.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', TeacherViews.update_attendance_data, name="update_attendance_data"),
    path('teacher_class_register/', TeacherViews.teacher_class_register, name="teacher_class_register"),
    path('teacher_class_register_save/', TeacherViews.teacher_class_register_save, name="teacher_class_register_save"),
    path('teacher_feedback/', TeacherViews.teacher_feedback, name="teacher_feedback"),
    path('teacher_feedback_save/', TeacherViews.teacher_feedback_save, name="teacher_feedback_save"),
    path('teacher_profile/', TeacherViews.teacher_profile, name="teacher_profile"),
    path('teacher_profile_update/', TeacherViews.teacher_profile_update, name="teacher_profile_update"),
    path('teacher_add_result/', TeacherViews.teacher_add_result, name="teacher_add_result"),
    path('teacher_add_result_save/', TeacherViews.teacher_add_result_save, name="teacher_add_result_save"),
    path('add_online_class/', TeacherViews.add_online_class, name="add_online_class"),
    path('get_online_class/', TeacherViews.get_online_class, name="get_online_class"),
    path('get_exams/', TeacherViews.get_exams, name="get_exams"),
    path('play_class/<class_id>/', TeacherViews.play_class, name="play_class"),
    path('pause_class/<class_id>/', TeacherViews.pause_class, name="pause_class"),
    path('delete_online_class/<class_id>/', TeacherViews.delete_class, name="delete_online_class"),
    path('get_exam_students/', TeacherViews.get_exam_students, name="get_exam_students"),
    path('check_attendance_exist/', TeacherViews.check_attendance_exist, name="check_attendance_exist"),
    path('check_class_reg_exist/', TeacherViews.check_class_reg_exist, name="check_class_reg_exist"),
    
    path('manage_assigned_classes/', TeacherViews.manage_assigned_classes, name="manage_assigned_classes"),

##########


    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    ##
    path('student_apply_payment/', StudentViews.student_apply_payment, name="student_apply_payment"),
    path('student_apply_payment_save/', StudentViews.student_apply_payment_save, name="student_apply_payment_save"),
    path('view_notices/', StudentViews.view_notices, name="view_notices"),
    path('make_payment/<payment_id>/', StudentViews.make_payment, name="make_payment"),
    ##
    

    
    path('student_get_payment_date/', StudentViews.student_get_payment_date, name="student_get_payment_date"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
    path('online_class/', StudentViews.online_class, name="online_class"),
    path('get_student_report_card/', StudentViews.get_student_report_card , name="get_student_report_card"),




    # URSL for Accountant
    path('accountant_home/', AccountantViews.accountant_home, name="accountant_home"),
    path('accountant_get_students_fees/', AccountantViews.get_students_fees, name="accountant_get_students_fees"),
    path('accountant_take_fees/', AccountantViews.take_fees, name="accountant_take_fees"),
    path('accountant_save_fees_data/', AccountantViews.save_fees_data, name="accountant_save_fees_data"),
    path('accountant_get_fees_dates/', AccountantViews.get_fees_dates, name="accountant_get_fees_dates"),
    path('accountant_update_fees/', AccountantViews.update_fees, name="accountant_teacher_update_fees"),  
    path('accountant_get_fees_student/', AccountantViews.get_fees_student, name="accountant_get_fees_student"),
    path('accountant_update_fees_data/', AccountantViews.update_fees_data, name="accountant_update_fees_data"),
    path('accountant_teacher_payment_date_filter/', AccountantViews.accountant_teacher_payment_date_filter, name="accountant_teacher_payment_date_filter"),
    # path('accountant_teacher_payment_all/', AccountantViews.accountant_teacher_payment_all, name="accountant_teacher_payment_all"),
    path('accountant_teacher_payment_date_filter_single/', AccountantViews.accountant_teacher_payment_date_filter_single, name="accountant_teacher_payment_date_filter_single"),
    path('accountant_add_teachers_payment/', AccountantViews.accountant_add_teachers_payment, name="accountant_add_teachers_payment" ),
    path('accountant_student_apply_payment/', AccountantViews.accountant_student_apply_payment, name="accountant_student_apply_payment"),
    path('accountant_student_apply_payment_save/', AccountantViews.accountant_student_apply_payment_save, name="accountant_student_apply_payment_save"),
    path('accountant_get_student_payment/', AccountantViews.accountant_get_student_payment, name="accountant_get_student_payment"),
    path('accountant_add_student_payment/<payment_id>/', AccountantViews.accountant_add_student_payment, name="accountant_add_student_payment"),
    path('accountant_expenses/', AccountantViews.accountant_expenses, name="accountant_expenses"),
    path('accountant_get_expenses/', AccountantViews.accountant_get_expenses, name="accountant_get_expenses"),
    path('accountant_add_expenses/', AccountantViews.accountant_add_expenses, name="accountant_add_expenses"),
    path('accountant_download-invoice/<payment_id>/', AccountantViews.accountant_download_invoice_view,name='accountant_download-invoice'),
    # path('accountant_get_students_for_payment', AccountantViews.accountant_get_students_for_payment , name="accountant_get_students_for_payment"),
    
    



]

