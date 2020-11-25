from django.db import models
from django.contrib import admin

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class AccountType(models.Model):
    account_type = models.CharField(primary_key=True, max_length=10)
    price = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'account_type'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Biomass(models.Model):
    inst = models.OneToOneField('Installations', models.DO_NOTHING, primary_key=True)
    methane = models.CharField(max_length=10)
    conversionmethod = models.CharField(db_column='conversionMethod', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'biomass'


class Client(models.Model):
    c = models.OneToOneField('Stakeholder', models.DO_NOTHING, primary_key=True)
    occupation = models.CharField(max_length=10)
    account_type = models.ForeignKey(AccountType, models.DO_NOTHING, db_column='account_type')

    class Meta:
        managed = False
        db_table = 'client'


class Credentials(models.Model):
    uname = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)
    id = models.ForeignKey('Stakeholder', models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'credentials'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    e = models.OneToOneField('Stakeholder', models.DO_NOTHING, primary_key=True)
    dept = models.CharField(max_length=10)
    manages = models.ForeignKey('self', models.DO_NOTHING, db_column='manages',null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Geothermal(models.Model):
    inst = models.OneToOneField('Installations', models.DO_NOTHING, primary_key=True)
    flowrate = models.DecimalField(db_column='flowRate', max_digits=5, decimal_places=0)  # Field name made lowercase.
    temp = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'geothermal'


class Hydro(models.Model):
    inst = models.OneToOneField('Installations', models.DO_NOTHING, primary_key=True)
    river = models.CharField(max_length=20)
    height = models.DecimalField(max_digits=20, decimal_places=2)
    length = models.DecimalField(max_digits=20, decimal_places=2)
    damname = models.CharField(db_column='damName', max_length=20)  # Field name made lowercase.
    currlevel= models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'hydro'


class Installations(models.Model):
    inst_id = models.CharField(primary_key=True, max_length=5)
    c = models.ForeignKey('Stakeholder', models.DO_NOTHING)
    capacity = models.CharField(max_length=10)
    gps = models.CharField(max_length=30)
    status = models.CharField(max_length=5)
    efficiency = models.DecimalField(max_digits=3, decimal_places=0)
    la = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    lo = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'installations'


class Invoice(models.Model):
    invoice_id = models.CharField(primary_key=True, max_length=5)
    service_type = models.ForeignKey('Services', models.DO_NOTHING, db_column='service_type')
    c = models.ForeignKey(Client, models.DO_NOTHING)
    e = models.ForeignKey(Employee, models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'invoice'


class LCity(models.Model):
    city = models.CharField(primary_key=True, max_length=20)
    state = models.ForeignKey('LState', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'l_city'


class LState(models.Model):
    state = models.CharField(primary_key=True, max_length=20)
    country = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'l_state'


class Phone(models.Model):
    id = models.ForeignKey('Stakeholder',models.DO_NOTHING,db_column='id')
    phoneno = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'phone'


class Reporttime(models.Model):
    date = models.DateField()
    time = models.TimeField()
    report = models.ForeignKey('Reportlist', models.DO_NOTHING,primary_key=True)

    class Meta:
        managed = False
        db_table = 'reportTime'


class Reportlist(models.Model):
    report_id = models.CharField(primary_key=True, max_length=5)
    c = models.ForeignKey(Client, models.DO_NOTHING)
    total_efficiency = models.DecimalField(max_digits=5, decimal_places=2)
    investment = models.DecimalField(max_digits=10, decimal_places=0)
    monthly_avg = models.DecimalField(max_digits=5, decimal_places=2)
    proft_loss = models.DecimalField(max_digits=3, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'reportlist'


class Serviced(models.Model):
    serviced_id = models.CharField(primary_key=True, max_length=5)
    c = models.ForeignKey(Client, models.DO_NOTHING)
    e = models.ForeignKey(Employee,models.DO_NOTHING)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'serviced'


class Services(models.Model):
    service_type = models.CharField(primary_key=True, max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'services'


class Solar(models.Model):
    inst = models.OneToOneField(Installations, models.DO_NOTHING, primary_key=True)
    quantity_of_panels = models.DecimalField(max_digits=5, decimal_places=0)
    cloud_cover = models.CharField(max_length=5)
    humidity = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'solar'


class Stakeholder(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    city = models.ForeignKey(LCity, models.DO_NOTHING, db_column='city')
    dob = models.DateField()

    class Meta:
        managed = False
        db_table = 'stakeholder'


class Tidal(models.Model):
    inst = models.OneToOneField(Installations, models.DO_NOTHING, primary_key=True)
    tidalpotential = models.DecimalField(db_column='tidalPotential', max_digits=5, decimal_places=0)  # Field name made lowercase.
    dimension = models.CharField(max_length=10)
    barragesize = models.DecimalField(db_column='barrageSize', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tidal'


class Wind(models.Model):
    inst = models.OneToOneField(Installations, models.DO_NOTHING, primary_key=True)
    rotorradius = models.DecimalField(db_column='rotorRadius', max_digits=6, decimal_places=2)  # Field name made lowercase.
    blade = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    windspeed = models.DecimalField(db_column='windSpeed', max_digits=4, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wind'
