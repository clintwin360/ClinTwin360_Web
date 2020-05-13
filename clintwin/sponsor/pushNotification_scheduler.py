from apscheduler.schedulers.background import BackgroundScheduler
from push_notifications.models import APNSDevice


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminder_notifications, 'interval', days=3)
    # scheduler.add_job(send_reminder_notifications, 'interval', seconds=15)
    scheduler.start()


def send_reminder_notifications():
    devices = APNSDevice.objects.all()
    message = "Increase your chances of getting matched to new trials! Answer more questions now"
    for device in devices:
        try:
            device.send_message(message)
        except:
            pass


start()
