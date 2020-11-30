from django import forms
from django.contrib.auth.models import User
from manager.models import project_lead
from manager.models import members

roles=(("Project_lead","Project_lead"),("Project_member","Project_member"))
class userform(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-6',"placeholder":"First Name"}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-6',"placeholder":"Last Name"}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-6',"placeholder":"Username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control col-6',"placeholder":"Password"}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control col-6',"placeholder":"Email"}))
    class Meta:
        model=User
        fields=("first_name","last_name","email","username","password")

class NewuserForm(forms.ModelForm):
    role=forms.ChoiceField(choices=roles,widget=forms.Select(attrs={'class':'form-control col-6'}))
    class Meta:
        model = project_lead
        fields=("role",)


class project_form(forms.ModelForm):

    project = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-6', "placeholder": "Project Name"}))
    work_given = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-6', "placeholder": "Work Given"}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-6', "placeholder": "Describe"}))
    deadline = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control col-6', "placeholder": "YYYY-MM-DD"}))
    work_given_to=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-6', "placeholder": "None"}))


    class Meta:
        model=project_lead
        fields=("project","work_given","description","deadline","work_given_to")
