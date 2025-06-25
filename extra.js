// //  (AMD64)] on win32
// Type "help", "copyright", "credits" or "license" for more information.        
// (InteractiveConsole)
// >>> task1.taskdetail.priority
// Traceback (most recent call last):
//   File "<console>", line 1, in <module>
// NameError: name 'task1' is not defined. Did you mean: 'Task'?
// >>> exit()
// now exiting InteractiveConsole...
// (task_env) 
// sakir@Safayet MINGW64 /d/Django Project/Task Management (module-5)
// $ python manage.py makemigrations
// Migrations for 'tasks':
//   tasks\migrations\0006_alter_taskdetail_task.py
//     ~ Alter field task on taskdetail
// (task_env) 
// sakir@Safayet MINGW64 /d/Django Project/Task Management (module-5)
// $ python manage.py shell
// 10 objects imported automatically (use -v 2 for details).

// Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
// Type "help", "copyright", "credits" or "license" for more information.        
// (InteractiveConsole)
// >>> from tasks.models import *
// >>> task =Task.objects.get(id=1)
// >>> task.taskdetail
// Traceback (most recent call last):
//   File "<console>", line 1, in <module>
// AttributeError: 'Task' object has no attribute 'taskdetail'
// >>> tasks.taskdetails
// Traceback (most recent call last):
//   File "<console>", line 1, in <module>
// NameError: name 'tasks' is not defined. Did you mean: 'task'?
// >>> task.details
// <TaskDetail: TaskDetail object (1)>
// >>> task.details.priority
// 'K'
// >>> employee1=Employee.objects.get(id=1)
// >>> employee1
// <Employee: Employee object (1)>
// >>> employee.task_set
// Traceback (most recent call last):
//   File "<console>", line 1, in <module>
// NameError: name 'employee' is not defined. Did you mean: 'Employee'?
// >>> employee1.task_set
// <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x00000165145A4050>
// >>> employee1.task_set.all()
// <QuerySet [<Task: Task object (4)>]></locals>