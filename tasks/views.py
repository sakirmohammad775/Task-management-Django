from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task

# Create your views here.
def manager_dashboard(request):
    return render(request, 'dashboard/manager_dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user_dashboard.html')

def test(request):
    context={ 
        'names':['John',"ahmed","john"],
        'age':[25,30,35],
        'city':['cairo','alex','giza']
        
    }
    return render(request,'test.html',context)

def create_task(request):
    # employees=Employee.objects.all() # get all employees from database 
    form =TaskModelForm() #For Get
    
    if request.method=="POST": #For Post
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model form data"""
            form.save()
            return render(request,'task_form.html',{"form":form,"message":"task added successfully"})
            
            """For Django Form data"""
            # data=form.cleaned_data
            # title=data.get('title')
            # description=data.get('description')
            # due_date=data.get('due_date')
            # assigned_to=data.get('assigned_to')
            
            # task=Task.objects.create(title= title,description=description,due_date=due_date)
            
            # for emp_id in assigned_to:
            #     employee=Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            return HttpResponse('task created successfully')
        
    context={"form":form} # For Get
    return render(request,"task_form.html",context) # return the form to the user

def view_task( request):
    #Retrieve all tasks from database
    tasks=Task.objects.all()
    
    #Retrieve a specific task from database
    task_3=Task.objects.get(id=1)
    return render(request,'show_task.html',{'tasks':tasks,"task3":task_3})