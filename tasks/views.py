from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min
from django.contrib import messages



# Create your views here.
def manager_dashboard(request):

     # optimizing the query
    # # getting task views here
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()
    
    type = request.GET.get('type','all')
    print(type)
    
    counts = Task.objects.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="COMPLETED")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
        pending=Count("id", filter=Q(status="PENDING")),
    )
    # Retriving task data
    base_query = (
        Task.objects.select_related("details").prefetch_related("assigned_to")
    ) 
    if type=='completed':
        tasks=base_query.filter(status='COMPLETED')
    elif type=='in-progress':
        tasks=base_query.filter(status='IN_PROGRESS')
    elif type=='pending':
        tasks=base_query.filter(status='PENDING')
    elif type=='all':
        tasks=base_query.all()
        
    context = {"tasks": tasks, "counts": counts}
    return render(request, "dashboard/manager_dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")


def test(request):
    context = {
        "names": ["John", "ahmed", "john"],
        "age": [25, 30, 35],
        "city": ["cairo", "alex", "giza"],
    }
    return render(request, "test.html", context)

## create task
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()  # For GET
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

##update Task
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)  # For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

def delete_task(request,id):
    if request.method=='POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,'something error')
        return redirect('manager-dashboard')

def view_task(request):
    # tasks=Task.objects.all() # Retrieve all tasks from database
    # task_3=Task.objects.get(id=1) # Retrieve a specific task from database
    # tasks=Task.objects.filter(status="PENDING") #Filtering data
    # tasks=Task.objects.filter(due_date=date.today()) # Show date today tasks
    """Show the task whose priority is not low"""
    # tasks=TaskDetail.objects.exclude(priority="L")
    """Show the task which are pending or in-progress"""
    # tasks=Task.objects.filter(Q(status="PENDING")|Q(status="IN_PROGRESS"))

    # select_related(foreignKey,OneToOneField)
    # tasks=TaskDetail.objects.select_related('task').all() # Retrieve all tasks from database with details optimized way query
    # tasks=Task.objects.select_related('project').all()
    # tasks=Project.objects.prefetch_related('task_set').all() # prefetch used for many to many fields to reduce the sql time
    projects = Project.objects.annotate(num_task=Count("task")).order_by("num_task")
    return render(request, "show_task.html", {"projects": projects})
