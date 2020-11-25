from django.contrib import admin

# Register your models here.
from remsite.models import *

model = [Employee,Stakeholder,AccountType,Biomass,Client,Credentials,Geothermal,Hydro,Installations,Invoice,LCity,LState,Phone,Reporttime,Reportlist,Serviced,Services,Solar,Tidal,Wind]
admin.site.register(model)