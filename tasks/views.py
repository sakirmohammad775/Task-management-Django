from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import *
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator



# Create your views here.
#### class based views
class Greetings(View):
    greetings='hello everyone'
    def get(self,request):
        return HttpResponse (self.greetings)

class HiGreetings(Greetings):
    greetings='vala acenni'

def is_manager(user):
    return user.groups.filter(name="Manager").exists()


def is_employee(user):
    return user.groups.filter(name="Employee").exists()


@user_passes_test(is_manager, login_url="no-permission")
def manager_dashboard(request):
    type = request.GET.get("type")

    # total_task count
    # total_task=Task.objects.all().count()
    # pending_task= Task.objects.filter(status='PENDING').count()
    # completed_task= Task.objects.filter(status='COMPLETED').count()
    # in_progress= Task.objects.filter(status='IN_PROGRESS').count()

    # context={
    #     'tasks':tasks,
    #     "total_task":total_task,
    #     "pending_task":pending_task,
    #     "completed_task":completed_task,
    #     "in_progress":in_progress
    # }
    type = request.GET.get("type", "all")  # default value

    counts = Task.objects.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="PENDING")),
        completed=Count("id", filter=Q(status="COMPLETED")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
    )
    # retriving data from database
    base_query = (
        Task.objects.select_related("details").prefetch_related("assigned_to").all()
    )
    if type == "completed":
        tasks = base_query.filter(status="COMPLETED")
    elif type == "pending":
        tasks = base_query.filter(status="PENDING")
    elif type == "in-progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == "all":
        tasks = base_query.all()

    context = {"tasks": tasks, "counts": counts,"role":'manager'}

    return render(request, "dashboard/manager_dashboard.html", context)


@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")


@login_required
@permission_required("tasks.add_task", login_url="no-permission")
def create_task(request):
    # employees=Employee.objects.all() # get all employees from database
    task_form = TaskModelForm()  # For Get
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":  # For Post
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "task created successfully")
            return redirect("create_task")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}  # For Get
    return render(request, "task_form.html", context)  # return the form to the user


#variable for list of decorators
create_decorators=[login_required,permission_required(
    "tasks.add_task",login_url='no-permission')] ## used of all other 
"""class based view """
@method_decorator(create_decorators, name="dispatch")
class CreateTask(View):
    """ for creating task"""
    template_name ='task_form.html' ##
    
    def get(self,request,*args, **kwargs):
        task_form = TaskModelForm()  # For Get
        task_detail_form = TaskDetailModelForm()
        
        context = {"task_form": task_form, "task_detail_form": task_detail_form}  # For Get
        return render(request, self.template_name, context)  # return the form to the user
    
    def post(self,request,*args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "task created successfully")
            return redirect("create_task")
        
        

@login_required
@permission_required("tasks.change_task", login_url="no-permission")
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)  # For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """For Model Form Data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect("update_task", id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


@login_required
@permission_required("tasks.delete_task", login_url="no-permission")
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect("manager_dashboard")
    else:
        messages.error(request, "Something went wrong")
        return redirect("manager_dashboard")


@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def view_task(request):
    # retrive all tasks from database
    """prefetch_related reverse foreignkey,manytomany"""
    tasks = Task.objects.prefetch_related("assigned_to").all()
    return render(request, "show_task.html", {"tasks": tasks})


@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choice = Task.STATUS_CHOICES

    if request.method == "POST":
        selected_status = request.POST.get("task_status")
        print(selected_status)
        task.status = selected_status
        task.save()
        return redirect("task-details", task.id)
    return render(
        request, "task_details.html", {"task": task, "status_choices": status_choice}
    )

login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect("manager_dashboard")
    elif is_employee(request.user):
        return redirect("user-dashboard")
    elif is_admin( request.user):
        return redirect("admin-dashboard")
    return redirect('no-permission')