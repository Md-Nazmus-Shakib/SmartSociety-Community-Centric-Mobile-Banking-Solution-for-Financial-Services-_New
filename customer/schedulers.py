from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events

def auto_task():
    print("Running scheduled task...")
    
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_task, 'interval', seconds=1500)
    register_events(scheduler)
    scheduler.start()
    