from django.db import models
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.core.mail import send_mail
from django.dispatch import receiver

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):  # pragma: no cover
        return self.name


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "pending"),
        ("IN_PROGRESS", "in progress"),
        ("COMPLETED", "completed"),
    ]
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, default=1
    )  # One to many relationship (child=task... parent=project)

    assigned_to = models.ManyToManyField(
        Employee, related_name="tasks"
    )  # many to many field (one employee can have many tasks) and one task can be assigned to many employees

    # new_string=models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


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
    # std_id=models.CharField( max_length=100, unique=True)
    task = models.OneToOneField(
        Task,
        on_delete=models.DO_NOTHING, 
        related_name="details")
    
    # one to one relationship
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details from Task{self.task.title}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name

# signals m-11 send signal to the receiver in terminal  
@receiver(m2m_changed,sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender,instance,action,**kwargs):
    if action=='post_add':
        print(instance,instance.assigned_to.all())
        assigned_emails=[emp.email for emp in instance.assigned_to.all()]
        
        send_mail(
            "New Task Assigned",
            f"you have been assigned to {instance.title}",
            "aislash05@gmail.com",
            assigned_emails,
            fail_silently=False
        )

@receiver(post_delete,sender=Task)
def delete_associate_details(sender,instance,**kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()
        
        print('deleted successfully')