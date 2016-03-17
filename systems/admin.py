from django.contrib import admin
from .models import Runner, System, Fund, SystemSnapshot, FundSnapshot
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from useraccounts.models import UserProfile

# Register your models here.
admin.site.register([Runner, System, Fund, SystemSnapshot, FundSnapshot])

class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInLine, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class RunnerAdmin(admin.ModelAdmin):
    list_filter = ('raceno', 'racedate','FINALPOS', 'bfsp', 'runtype', 'racecoursename')
    search_fields = ('raceno', 'racedate', 'jockeyname', 'trainername')
    date_hierarchy= 'racedate'
