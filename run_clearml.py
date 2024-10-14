import clearml

project = 'Demo'
task_name = 'joblib zombie'
docker_image = 'registry.pyn.ru/python3.9-kardinal-clearml:2024.03.11'
repo = 'git@github.com:/amishurov/joblib_zombie'

task = clearml.Task.init(project_name=project, task_name=task_name)
task.set_base_docker(
    docker_image=docker_image,
)
task.set_repo(repo=repo, branch='master')
task.set_script(entry_point='main.py')
task.execute_remotely(queue_name='default')
