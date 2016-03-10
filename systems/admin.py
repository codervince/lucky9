from django.contrib import admin
from .models import Runner, System, Snapshot, Fund, Investment, SystemSnapshot, FundSnapshot, QueryClause


# Register your models here.
admin.site.register([Runner, System, Snapshot, Fund, Investment, SystemSnapshot, FundSnapshot, QueryClause])

class RunnerAdmin(admin.ModelAdmin):
    list_filter = ('raceno', 'racedate','FINALPOS', 'bfsp', 'runtype', 'racecoursename')
    search_fields = ('raceno', 'racedate', 'jockeyname', 'trainername')
    date_hierarchy= 'racedate'
