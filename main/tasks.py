from apscheduler.schedulers.blocking import BlockingScheduler
from .parser import function


class periodic_task:
    
    __task= None
    __task_instance=None
    
    def __init__(self,time=60):
        periodic_task.__task=BlockingScheduler()
        periodic_task.__task_instance=periodic_task.__task.add_job(function,'interval',seconds=time,id='my_task')

    def __str__(self):
        return "Task_scheduler"

    def run(self):
        periodic_task.__task.start()
        
    def remove_task(self):
        periodic_task.__task_instance.remove()
        
    def pause_task(self):
        periodic_task.__task_instance.pause()
        
    def resume_task(self):
        periodic_task.__task_instance.resume()
        
    def sut_down_scheduler(self):
        periodic_task.__task.shutdown()
        
    def modify_task(self,time):
        periodic_task.__task.reschedule_job('my_task',trigger='interval',minute=time)