from datetime import datetime
from typing import ContextManager
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import request
from remsite.models import AccountType, AuthGroup, Biomass, Client, Credentials, Employee, Geothermal, Hydro, Installations, Invoice, LCity, LState, Phone, Reportlist, Reporttime, Serviced, Services, Solar, Stakeholder, Tidal, Wind
from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User,auth
from sequences import get_next_value


def home(request):
    return render(request,"home.html")

def editdetails(request):
    return render(request,"editdetails.html")


def features(request):
    return render(request,"features.html")


def team(request):
    return render(request,"team.html")

def editsubmission(request):
    loggedinUname=request.user.username
    loggedinID=Credentials.objects.get(uname=loggedinUname).id.id
    curr=Stakeholder.objects.get(id=loggedinID)
    e=request.POST['email']
    if(e != ''):
        email = request.POST['email']
        curr.email=email
    c=request.POST['city']
    if(c != ''):
        cityx = request.POST['city']
        statex = request.POST['state']
        countryx = request.POST['country']
        if LState.objects.filter(state=statex,country=countryx).exists():
            pass
        else:
            LState.objects.create(state=statex,country=countryx)

        if LCity.objects.filter(city=cityx,state=statex).exists():
            pass
        else:
            LCity.objects.create(city=cityx,state=LState.objects.get(state=statex,country=countryx))
        cityob=LCity.objects.get(city=cityx,state=LState.objects.get(state=statex,country=countryx))
        curr.city=cityob
    curr.save()


    curr=Client.objects.get(c=loggedinID)
    o=request.POST['occupation']
    if(o != ''):
        occupationx = request.POST['occupation']
        curr.occupation=occupationx
    if('types' not in request.POST):
        pass
    else:
        t=request.POST['types']
        if(t != ''):
            atype = request.POST['types']
            curr.account_type=AccountType.objects.get(account_type=atype.lower())
            cost=0
            if atype=='business':
                cost=299
            elif atype=='standard':
                cost=99
            else:
                cost=199
            ob=Reportlist.objects.get(c=loggedinID)
            currinv=ob.investment
            currinv+=int(cost)
            ob.investment=currinv
            ob.save()
            ident=request.user.username
            credid=Credentials.objects.get(uname=ident).id.id
            client=Client.objects.get(c=credid)
            service_type='Account plan'
            service_type=Services.objects.get(service_type=service_type)
            Invoice.objects.create(invoice_id=get_next_value("invoice"),service_type=service_type,c=client,total_price=cost)

    curr.save()

    p=request.POST['phoneno']

    if(p != ''):
        phone = request.POST['phoneno']
        Phone.objects.create(id=Stakeholder.objects.get(id=loggedinID),phoneno=phone)
    messages.info(request,'Account details have been updated.')

    pa=request.POST['password1']
    if(pa != ''):
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1!=password2):
            messages.info(request,'Passwords are not matching!')
            return redirect('editdetails')
        user=User.objects.get(username=loggedinUname)
        user.set_password(password1)
        user.save()
        curr=Credentials.objects.get(id=loggedinID)
        curr.password=password1
        curr.save()
        auth.logout(request)
        return redirect('/')

    return render(request,"home.html")


def addInst(request):
    if(request.method=='POST'):
        
        type=request.POST['types']

        instidx = get_next_value("inst")
        instidx=str(instidx)
        instidx=list(instidx)
        instidx.append(type[0])
        instidx = "".join(instidx)
        loggedinUname=request.user.username
        loggedinID=Credentials.objects.get(uname=loggedinUname).id.id
        capacity = request.POST['cap']
        eff = request.POST['eff']
        loc = request.POST['loc']
        from geopy.geocoders import Nominatim
        geolocator=Nominatim(user_agent="rem")
        location=geolocator.geocode(loc)
        la= location.latitude
        lo= location.longitude
        status = request.POST['status']
        curr=Installations.objects.create(inst_id=instidx,c=Stakeholder.objects.get(id=loggedinID),capacity=capacity,gps=loc,status=status,efficiency=eff,la=la,lo=lo)
        if(type=='solar'):
            qop = request.POST['qop']
            hum = request.POST['hum']
            cc = request.POST['cc']
            Solar.objects.create(inst=curr,quantity_of_panels=qop,cloud_cover=cc,humidity=hum)
        if(type=='wind'):
            rr = request.POST['rr']
            br = request.POST['br']
            ws = request.POST['ws']
            Wind.objects.create(inst=curr,rotorradius=rr,blade=br,windspeed=ws)
        if(type=='hydro'):
            river = request.POST['river']
            damn = request.POST['damn']
            height = request.POST['height']
            length = request.POST['length']
            currlvl= request.POST['currlvl']
            Hydro.objects.create(inst=curr,river=river,height=height,length=length,damname=damn,currlevel=currlvl)

        if(type=='geo'):
            flow = request.POST['flow']
            inttemp = request.POST['inttemp']
            Geothermal.objects.create(inst=curr,flowrate=flow,temp=inttemp)
        if(type=='tidal'):
            tidalpot = request.POST['tidalpot']
            dim = request.POST['dim']
            barragesize = request.POST['barragesize']
            Tidal.objects.create(inst=curr,tidalpotential=tidalpot,dimension=dim,barragesize=barragesize)
        if(type=='bio'):
            methane = request.POST['methane']
            conme = request.POST['conme']
            Biomass.objects.create(inst=curr,methane=methane,conversionmethod=conme)
        messages.info(request,'Installation Created')

        return redirect('addInst') 
    else:
        
        return render(request,"addInst.html")

def viewInst(request):

    loggedinUname=request.user.username
    loggedinID=Credentials.objects.get(uname=loggedinUname).id.id
    inst=Installations.objects.filter(c=loggedinID)
    solar=None
    wind=None
    hydro=None
    tidal=None
    bio=None
    geo=None
    la=[]
    lo=[]
    for i in inst:
        if(i.inst_id[-1]=='s'):
            solar=Solar.objects.filter(inst=i.inst_id)
        elif(i.inst_id[-1]=='w'):
            wind=Wind.objects.filter(inst=i.inst_id)
        elif(i.inst_id[-1]=='h'):
            hydro=Hydro.objects.filter(inst=i.inst_id)
        elif(i.inst_id[-1]=='b'):
            bio=Biomass.objects.filter(inst=i.inst_id)
        elif(i.inst_id[-1]=='g'):
            geo=Geothermal.objects.filter(inst=i.inst_id)
        else:
            tidal=Tidal.objects.filter(inst=i.inst_id)
        la.append(None if i.la is None else float(i.la))
        lo.append(None if i.lo is None else float(i.lo))


    leng=len(inst)
    la = json.dumps(la)
    lo = json.dumps(lo)
    

    context={ "la":la,"lo":lo,"leng":leng,"inst": inst,"solar":solar,"wind":wind,"hydro":hydro,"bio":bio,"geo":geo,"tidal":tidal}
    return render(request,"viewInst.html",context)

def account(request):
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    stake=Stakeholder.objects.get(id=credid)
    client=Client.objects.get(c=credid)
    phoneno=Phone.objects.filter(id=credid)

  

    context={"stake":stake,"client":client,"phone":phoneno}
    return render(request,"account.html",context)

    
def plans(request):
    return render(request,'plans.html')



def callouts(request):
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    if(Client.objects.get(c=credid).account_type.account_type=='standard'):
        messages.info(request,'Your plan is not eligible for Alerts and Callouts. Please consider upgrading your plan to get frequent callouts.')
        return redirect('/')
    inst=Installations.objects.filter(c=credid)
    callout=[]
    for i in inst:
        if (i.efficiency<=25 and i not in callout):
            callout.append(i)
        if(i.status.lower() =='inactive' and i not in callout):
            callout.append(i)
    if(len(callout)==0):
        messages.info(request,'All your installations are working well. There are no alerts.')
        return redirect('/')
    context={"callout":callout}

    return render(request,'callouts.html',context)



def reports(request):
    
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    inst=Installations.objects.filter(c=credid)
    avgeff=0
    count=0
    repid=Reportlist.objects.get(c=credid).report_id
    for i in inst:
        count+=1
        avgeff+=i.efficiency
    if(count!=0):
        avgeff/=count
        avgeff=int(avgeff)
        at=Client.objects.get(c=credid).account_type.account_type
        inv=AccountType.objects.get(account_type=at).price
        if(Reportlist.objects.filter(c=credid).exists()):
            repp=Reportlist.objects.get(report_id=repid)
            repp.total_efficiency=avgeff
            repp.save()
            repinfo=Reportlist.objects.get(c=credid)
            context={"repinfo":repinfo}
            return render(request,'reports.html',context)

    messages.info(request,'You do not own any installation and so, we cannot create any reports for you.')
    return redirect("/")
    



    
def contactus(request):
  
    
    return render(request,'contactus.html')

def services(request):
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    if(Client.objects.get(c=credid).account_type.account_type=='standard'):
        messages.info(request,'Your plan is not eligible for services. Please consider upgrading your plan to experience our service.')
        return redirect('/')

    if(Reportlist.objects.filter(c=credid).exists()):
        slist=Services.objects.all()
        slist=slist.exclude(service_type="Account plan")
        context={"slist":slist}
        return render(request,'services.html',context)
    else:
        messages.info(request,'You do not own any installations and so we can not provide you any services.')
        return redirect('/')



def bookser(request):
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    client=Client.objects.get(c=credid)
    cost=request.POST['cost']
    service_type=request.POST['service_type']
    service_type=Services.objects.get(service_type=service_type)
    ob=Reportlist.objects.get(c=credid)
    repid=ob.report_id
    currinv=ob.investment
    currinv+=int(cost)
    ob.investment=currinv
    ob.save()

    from datetime import date,datetime
    dates=date.today().strftime("%Y-%m-%d")
    time=datetime.now().strftime("%H:%M:%S")
    obj=Reporttime.objects.get(report_id=repid)
    obj.time=time
    obj.date=dates
    obj.save()

    import random
    eids=Employee.objects.all()
    eid=random.choice(eids)
    Serviced.objects.create(serviced_id=get_next_value("serviced"),c=client,e_id=eid,date=dates)

    Invoice.objects.create(invoice_id=get_next_value("invoice"),service_type=service_type,c=client,e=eid,total_price=cost)
    messages.info(request,'Service Booked')



    return redirect('services')

def invoice(request):
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    invoiceforhim=(Invoice.objects.filter(c=credid))
    stake=Stakeholder.objects.get(id=credid)
    totalcost=Reportlist.objects.get(c=credid).investment
    date=datetime.now()
    context={"invoiceforhim":invoiceforhim,"client":stake,"totalcost":totalcost,"date":date}
    return render(request,"invoice.html",context)


def callmail(request):
    ident=request.user.username
    credid=Credentials.objects.get(uname=ident).id.id
    inst=Installations.objects.filter(c=credid)
    stake=Stakeholder.objects.get(id=credid)
    callout=[]
    for i in inst:
        if (i.efficiency<=25 and i not in callout):
            callout.append(i)
        if(i.status.lower() =='inactive' and i not in callout):
            callout.append(i)
    from django.core.mail import send_mail
    subj=''
    for i in callout:
        if i.efficiency <= 25:
            subj+='The efficiency of your installation ' +  str(i.inst_id)  + ' is less at a rate of ' + str(i.efficiency)  + '.\n'
        if i.status.lower() == 'inactive':
            subj+='Your installation ' +   str(i.inst_id) +' is inactive now.\n'
    send_mail(
    'REM Alert',
     subj,
    'remgescbe@gmail.com',
    [stake.email],
    fail_silently=False,)
    messages.info(request,'Mail sent')
    return redirect('callouts')

def turnoninst(request):
    inst=request.POST['idon']
    ob=Installations.objects.get(inst_id=inst)
    ob.status='active'
    ob.save()
    return redirect('/viewInst')


def turnoffinst(request):
    inst=request.POST['idoff']
    ob=Installations.objects.get(inst_id=inst)
    ob.status='inactive'
    ob.save()
    return redirect('viewInst')
