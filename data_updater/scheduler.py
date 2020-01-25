from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#### Blocking scheduler runs at foreground, disabling the django app. So use BackgroundScheduler
# frosm apscheduler.schedulers.blocking import BlockingScheduler 
from data_updater import dataApi

def start():
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(dataApi._pull_and_update, 'interval', day=1)
    # scheduler.start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(dataApi._pull_and_update, 'cron',day_of_week='mon-fri', hour='8,11,12')
    scheduler.start()