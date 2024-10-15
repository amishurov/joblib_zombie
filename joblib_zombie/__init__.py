import time
import os
import clearml

CLEARML_TASK_ID = os.environ.get('CLEARML_TASK_ID')
clearml_task = clearml.Task.init()

def nope_function(task):
    if task == 4:
        raise Exception("Error in parallel job")
    else:
        time.sleep(task)
