from django.apps import AppConfig


class FastAppConfig(AppConfig):
    name = 'fast_app'

    ##### This is where you run your own py file!!
    def ready(self):
        from data_updater import scheduler, dataApi
        #### Run once when django is started, then run the scheduler
        dataApi._pull_and_update()       
        # scheduler.start()