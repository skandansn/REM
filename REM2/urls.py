"""REM2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from datetime import date
from random import randint
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from remsite.models import *
from background_task import background


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('remsite.urls')),
    path('auth/',include('auth.urls'))
    
]

@background()
def datagiver():
    inst=Installations.objects.all()
    solar=Solar.objects.all()
    wind=Wind.objects.all()
    hydro=Hydro.objects.all()
    bio=Biomass.objects.all()
    geo=Geothermal.objects.all()
    tidal=Tidal.objects.all()
    import random
    for i in solar:
        i.cloud_cover=random.randint(10,100)
        i.humidity=random.randint(10,90)
        i.save()

    for i in wind:
        i.windspeed=random.randint(40,75)
        i.save()

    for i in hydro:
        i.currlevel=random.randint(1000,10000)
        i.save()

    for i in bio:
        i.methane=random.randint(50,1000)
        i.save()
    
    for i in geo:
        i.flowrate=random.randint(50,1000)
        i.temp=random.randint(50,1000)
        i.save()

    

        
    return None

datagiver()
        

    

