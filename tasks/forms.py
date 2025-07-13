from django import forms
from tasks.models import Task
#Django Form(not used in future )
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(
        widget=forms.SelectDateWidget, label="Due Date"
    )  # select date widget is used to select date from calendar
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,choices=[],label="Assigned To")

    def __init__(self, *args, **kwargs): #fetching choices from database 
        employees = kwargs.pop("employees", [])  ## passing employees list from view
        super().__init__(*args, **kwargs)  # Call to the parent class's constructor
        self.fields["assigned_to"].choices = [(emp.id, emp.name) for emp in employees] # assigning choices to field


#Django Model Form
class TaskModelForm(forms.ModelForm): # ModelForm is used to create form from model
    class Meta: # Meta class is used to define fields and widgets
        model = Task # model is the model we are using
        fields =['title','description','due_date','assigned_to'] # fields are the fields we want to display in
        