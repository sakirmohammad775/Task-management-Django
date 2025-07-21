from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min


# Create your views here.
def manager_dashboard(request):
    type = request.GET.get('type')
    print(type)
     # optimizing the query
    # # getting task views here
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()
    tasks = (
        Task.objects.select_related("details").prefetch_related("assigned_to").all()
    ) 
    
    counts = Task.objects.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="COMPLETED")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
        pending=Count("id", filter=Q(status="PENDING")),
    )
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


def create_task(request):
    # employees=Employee.objects.all() # get all employees from database
    form = TaskModelForm()  # For Get

    if request.method == "POST":  # For Post
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model form data"""
            form.save()
            return render(
                request,
                "task_form.html",
                {"form": form, "message": "task added successfully"},
            )

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
            return HttpResponse("task created successfully")

    context = {"form": form}  # For Get
    return render(request, "task_form.html", context)  # return the form to the user


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
