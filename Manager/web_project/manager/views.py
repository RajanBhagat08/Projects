from django.shortcuts import render
from manager.models import project_lead,members
from django.contrib.auth.models import User
from manager.forms import NewuserForm,userform,project_form # booking_form_student
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import cache_control
from datetime import date
# Create your views here.
def index(request):
    return render(request,'manager/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required(login_url='/manager/user_login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def date_valid(date_req):   
    if date_req>=date.today():
        return True
    else:
        return False



def user_info_view(request):
        registered=False
        if request.method == 'POST':
            def_form=userform(data=request.POST)
            form = NewuserForm(request.POST)

            if form.is_valid() and def_form.is_valid():

                user=def_form.save()
                user.set_password(user.password)
                user.save()

                user_extra= form.save(commit=False)
                user_extra.user=user
                user_extra.save()


                registered=True
                return HttpResponseRedirect("/manager/thanks")

            else:
                print(form.errors)

        else:
            form=NewuserForm()
            def_form=userform()
            registered=False

        return render(request,'manager/register.html',{'def_form':def_form,
        'form':form,'registered':registered
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):

    if request.method=='POST':
        username= request.POST.get('username')
        password=request.POST.get('password')

        role=request.POST.get("role")
        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                print(role)
                if role=='project_lead':
                    return HttpResponseRedirect("/manager/home_lead/")
                elif role=="project_mem":
                    return HttpResponseRedirect("/manager/home_mem/")

            else: return HttpResponse("NOT Active")

        else:
            print("username: {} password: {}".format(username,password))
            logout(request)
            return HttpResponse("invalid login")

    else:
        return render(request,'manager/login.html',{})

def no_entry(request):
    return render(request, 'manager/no_entry.html',{})

@login_required
def home_mem(request):
    try:
        temp=members.objects.filter(user=request.user).order_by('deadline')
        dict={}
        for each in temp:
            if each.is_done==False:
                da_dict={
                    "project":each.project,"task":each.task,"head":each.head,"deadline": each.deadline
                }
                break
        if request.method=="POST":
            value=request.POST.get("approve")
        if value=="yes":
            each.is_done=True
            each.save()
            try:
                cemp=project_lead.objects.filter(project=each.project).filter(work_given=each.task)
                
                for i in cemp:
                    print("ethe hai ",i.user)
                    i.isdone=True
                    i.save()
            except:
                print("no record")

            return HttpResponseRedirect("/manager/home_mem")
        else:
            pass
            return HttpResponseRedirect("/manager/home_mem")



    except:
        print("no work")

    try:
        return render(request, 'manager/home_mem.html', da_dict)
    except UnboundLocalError:
        return HttpResponseRedirect("/manager/no_entry")

@login_required
def home_lead(request):
    assigned=False
    not_exist=False
    if request.method == 'POST':
            def_form=project_form(data=request.POST)

            if def_form.is_valid():

                user_to=def_form.cleaned_data.get("work_given_to")
                task_in=def_form.cleaned_data.get("work_given")
                project_in=def_form.cleaned_data.get("project")
                head_in=request.user
                deadline_in=def_form.cleaned_data.get("deadline")
                if(date_valid(deadline_in)==False):
                    return HttpResponse("oops!! This Date isn't valid now. Go back and change the date.")
                try:
                    
                    temp=User.objects.get(username=user_to)
                    print(type(temp.username))
                    entry=members(user=temp, task=task_in,project=project_in,head=head_in,deadline=deadline_in)
                    entry.save()
                    form1=def_form.save()
                    form1.user=request.user
                    form1.save()
                    assigned=True
                    return HttpResponse("work assigned!")
                except:
                    not_exist=True
            

            else:
                print(form.errors)

    else:
        def_form=project_form()
        assigned=False
    return render(request, 'manager/home_lead.html', {'def_form':def_form,'assigned':assigned,"not_exist":not_exist})

def thanks(request):
    return render(request, 'manager/thanks.html', {})


def completed(request):
    usernam=request.user.username
    approved_forms=project_lead.objects.filter(user__username__exact=usernam,isdone=True)
    return render(request,"manager/completed.html",{"approved_forms":approved_forms})

def yet_to_completed(request):
    usernam=request.user.username
    approved_forms=project_lead.objects.filter(user__username__exact=usernam,isdone=False)
    return render(request,"manager/yet_to_completed.html",{"approved_forms":approved_forms})

