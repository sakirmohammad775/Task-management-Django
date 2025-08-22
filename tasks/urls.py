from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,create_task,view_task,update_task,delete_task,task_details,dashboard,HiGreetings,CreateTask
urlpatterns=[
   path('manager_dashboard/',manager_dashboard,name= 'manager_dashboard'),
   path('user_dashboard/',employee_dashboard,name='user-dashboard'),
   # path('create_task/',create_task,name='create_task'),
   path('create_task/',CreateTask.as_view(),name='create_task'),
   path('view_task/',view_task),
   path('task/<int:task_id>/details/',task_details,name='task-details'),
   path('update_task/<int:id>/', update_task, name='update_task'),
   path('delete_task/<int:id>/', delete_task, name='delete_task'),
   path('dashboard',dashboard,name='dashboard'),
   
   path('greetings/',HiGreetings.as_view(),name='greetings')
]