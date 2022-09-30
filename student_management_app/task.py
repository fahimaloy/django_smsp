from .models import Teachers , Payment_Teacher
import datetime
def add_mothly_payment_task():
    teacher_obj = Teachers.objects.filter(monthly_payment_type=True)
    for teacher in teacher_obj:
        payment = Payment_Teacher(paying_date=datetime.datetime.now() + datetime.timedelta(days=10),teacher_id=teacher,payment_amount=teacher.monthly_payment,payment_upto=datetime.datetime.now() - datetime.timedelta(days=1),paid=False)
        payment.save()
        print("Task Done")
times=[1,3,10]
def app():
    print("Yayyyy")
from apscheduler.schedulers.background import BackgroundScheduler
import random
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(app,'interval',seconds=times[random.randint(0, 2)])
    scheduler.start()
    # pass