from apscheduler.schedulers.blocking import BlockingScheduler
from .parser import *
from .models import lecture


class periodic_task:
    
    __task= None
    __task_instance=None
    status=None
    
    def __init__(self,time=60):
        periodic_task.__task=BlockingScheduler()
        init_parsing()
        if periodic_task.__task_instance is None:
            periodic_task.__task_instance=periodic_task.__task.add_job(function,'interval',seconds=5)
        periodic_task.status="구동 중"
        periodic_task.__task.start()
        
        return

    def __str__(self):
        return "Task_scheduler"
        
    # def remove_task(self):
    #     periodic_task.__task_instance.remove()
    
    @classmethod
    def get_status(cls):
        return cls.status
    
    @classmethod   
    def pause_task(cls):
        cls.__task_instance.pause()
        cls.status="중단"
    
    @classmethod    
    def resume_task(cls):
        cls.__task_instance.resume()
        cls.status="구동 중"
        
    # def shut_down_scheduler(self):
    #     periodic_task.__task.shutdown()
    
    @classmethod
    def modify_task(cls,time=60):
        cls.__task_instance.reschedule(trigger='interval',seconds=time)