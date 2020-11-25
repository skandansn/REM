from random import random,randint

from django.core.mail import send_mail
from remsite.models import AccountType, Client, Credentials, LCity, LState, Phone, Reportlist, Reporttime, Stakeholder
from django.http import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from sequences import get_next_value


# Create your views here.


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password= request.POST['password']

        user=auth.authenticate(username=username,password=password)
        

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html')



def register(request):
    if(request.method=="POST"):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        cityx = request.POST['city']
        statex = request.POST['state']
        countryx = request.POST['country']
        dobx = request.POST['dob']
        occupationx = request.POST['occupation']
        phone = request.POST['phoneno']
        atype = request.POST['types']
        idx=get_next_value("id")   
        if(password1!=password2):
            messages.info(request,'Passwords are not matching!')
            return redirect('register')

        if Stakeholder.objects.filter(id=idx).exists():
            return redirect('register')

        if Credentials.objects.filter(uname=username).exists() or User.objects.filter(username=username).exists():
            messages.info(request,'The username you entered has already been taken. Please try another username.')
            return redirect('register')

        if LState.objects.filter(state=statex,country=countryx).exists():
            pass
        else:
            LState.objects.create(state=statex,country=countryx)

        if LCity.objects.filter(city=cityx,state=statex).exists():
            pass
        else:
            LCity.objects.create(city=cityx,state=LState.objects.get(state=statex,country=countryx))
        cityob=LCity.objects.get(city=cityx,state=LState.objects.get(state=statex,country=countryx))


        user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
        user.save()


        Stakeholder.objects.create(id=idx,fname=first_name,lname=last_name,city=cityob,dob=dobx,email=email)
        Credentials.objects.create(uname=username,password=password1,id=Stakeholder.objects.get(id=idx))
        Client.objects.create(c=Stakeholder.objects.get(id=idx),occupation=occupationx,account_type=AccountType.objects.get(account_type=atype.lower()))
        if(Phone.objects.filter(phoneno=phone).exists()):
            messages.info(request,'Phone number already linked with another account!')
            return redirect('register')
        else:
            pass


        Phone.objects.create(id=Stakeholder.objects.get(id=idx),phoneno=phone)
        repid = get_next_value("report")
        ident=user.username
        credid=Credentials.objects.get(uname=ident).id.id
        Reportlist.objects.create(report_id=repid,c=Client.objects.get(c=credid),total_efficiency=0,investment=0,monthly_avg=100,proft_loss=20)
        from datetime import date,datetime
        dates=date.today().strftime("%Y-%m-%d")
        Reporttime.objects.create(date=dates,time=datetime.now().strftime("%H:%M:%S"),report_id=repid)
        stake=Stakeholder.objects.get(id=credid)
        subj='Welcome to our REM community. Thank you for believing in us to manage your installations. Please login to our site to experience our services.'
        print('user_created')
        send_mail(
        'REM Alert',
        subj,
        'remgescbe@gmail.com',
        [stake.email],
        fail_silently=False,)
        return redirect('login')

    else:
        return render(request,"register.html")





def logout(request):
    auth.logout(request)
    return redirect('/')


