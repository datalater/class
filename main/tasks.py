from apscheduler.schedulers.blocking import BlockingScheduler
from .parser import function
from .models import lecture


class periodic_task:
    
    __task= None
    __task_instance=None
    status=None
    
    def __init__(self,time=60):
        periodic_task.__task=BlockingScheduler()
        if periodic_task.__task_instance is None:
            periodic_task.__task_instance=periodic_task.__task.add_job(function,'interval',seconds=5)
        periodic_task.status="구동 중"
        periodic_task.__task.start()
        
        return

    def __str__(self):
        return "Task_scheduler"
        
    # def remove_task(self):
    #     periodic_task.__task_instance.remove()
    
    @staticmethod
    def get_status():
        return periodic_task.status
    
    @staticmethod    
    def pause_task():
        periodic_task.__task_instance.pause()
        periodic_task.status="중단"
    
    @staticmethod    
    def resume_task():
        periodic_task.__task_instance.resume()
        periodic_task.status="구동 중"
        
    # def shut_down_scheduler(self):
    #     periodic_task.__task.shutdown()
    
    @staticmethod
    def modify_task(time=60):
        periodic_task.__task_instance.reschedule(trigger='interval',seconds=time)