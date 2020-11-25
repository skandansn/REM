from os import name
from remsite.views import callouts
from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('addInst',views.addInst,name='addInst'),
    path('viewInst',views.viewInst,name='viewInst'),
    path('account',views.account,name='account'),
    path('callouts',views.callouts,name='callouts'),
    path('reports',views.reports,name='reports'),
    path('plans',views.plans,name='plans'),
    path('contactus',views.contactus,name='contactus'),
    path('callmail',views.callmail,name='callmail'),
    path('bookser',views.bookser,name='bookser'),
    path('features',views.features,name='features'),
    path('team',views.team,name='team'),
    path('services',views.services,name='services'),
    path('invoice',views.invoice,name='invoice'),
    path('turnoninst',views.turnoninst,name='turnoninst'),
    path('turnoffinst',views.turnoffinst,name='turnoffinst'),
    path('editdetails',views.editdetails,name='editdetails'),
    path('editsubmission',views.editsubmission,name='editsubmission')



    
    ]
