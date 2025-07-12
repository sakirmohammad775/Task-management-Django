from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


# Create your models here.
class Task(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1) # One to many relationship (child=task... parent=project)

    assigned_to = models.ManyToManyField(Employee, related_name="tasks") # many to many field (one employee can have many tasks) and one task can be assigned to many employees

    # new_string=models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Task.object.get(id=2)
# ORM
# One to One
# One to many
# Many to many


class TaskDetail(models.Model):
    High = "H"
    Medium = "M"
    LOW = "L"
    PRIORITY_OPTIONS = (
        (High, "High"),
        (Medium, "Medium"),
        (LOW, "Low"),
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="details")
    # one to one relationship
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)


class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
