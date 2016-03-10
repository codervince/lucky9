from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    LANGUAGES =(
    ('en_US', 'English'),
    ('zh_HK', '中文'),
    ('zh_CN', '官话'),
    ('de_DE', 'Deutsch'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, choices=LANGUAGES) #iso code

#custom Manager
class LiveManager(models.Manager):
    def get_queryset(self):
        return super(LiveManager,self).get_queryset().filter(runtype='LIVE')


#based on CSV
class Runner(models.Model):
    objects = models.Manager()
    live = LiveManager()

    RUNTYPE = (
    ('LIVE', 'LIVE'),
    ('HISTORICAL', 'HISTORICAL'),
    )
    runtype = models.CharField(max_length=12, default='HISTORICAL')
    racedate = models.DateField()
    racecoursename = models.CharField(max_length=10)
    racecourseid = models.SmallIntegerField()
    racename = models.CharField(max_length=250)
    racetypehorse = models.CharField(max_length=10)
    racetypeconditions = models.CharField(max_length=10)
    racetypehs= models.CharField(max_length=10)
    ages = models.CharField(max_length=10)
    raceclass = models.CharField(max_length=10)
    distance = models.CharField(max_length=10)
    going = models.CharField(max_length=10)
    runners = models.SmallIntegerField()
    horsename = models.CharField(max_length=250)
    sirename = models.CharField(max_length=250)
    trainername = models.CharField(max_length=250)
    jockeyname = models.CharField(max_length=250)
    allowance = models.SmallIntegerField()
    FINALPOS = models.CharField(max_length=5)
    lbw = models.FloatField()
    winsp = models.FloatField() #may need to be converted
    winsppos = models.SmallIntegerField()
    bfsp = models.DecimalField(max_digits=6, decimal_places=2)
    bfpsp = models.DecimalField(max_digits=6, decimal_places=2)
    ratingrank = models.SmallIntegerField()
    rating = models.FloatField()
    raceno = models.CharField(max_length=250, unique=True)
    draw = models.SmallIntegerField()
    damname = models.CharField(max_length=250)
    damsirename  = models.CharField(max_length=250)
    racetime  = models.CharField(max_length=250)
    totalruns =  models.SmallIntegerField()
    placed = models.BooleanField()
    bfplaced= models.BooleanField()
    # systemid =  models.SmallIntegerField()


class Fund(models.Model):

    def get_absolute_url(self):
        return reverse('systems.fund_detail', args=[self.code])
    CURRENCIES = (
    ('AUD', 'AUD'),
    ('GBP', 'GBP'),
    )
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=30, unique=True)
    minimuminvestment = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250)
    longdescription = models.TextField()
    managementfee = models.FloatField()
    performancefee = models.FloatField()
    bailoutfee= models.FloatField()
    bettingratio = models.FloatField()
    sharespurchased = models.SmallIntegerField()
    initalshareissue = models.SmallIntegerField()
    costpershare = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCIES, default='GBP')
    openingbank = models.DecimalField(max_digits=7, decimal_places=2)
    currentbank = models.DecimalField(max_digits=7, decimal_places=2)
    currentprofit = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    investors = models.ManyToManyField(
        User,
        through='Investment',
        through_fields=('fund', 'user')
    )
    class Meta:
        ordering = ('-currentprofit',)

class Investment(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startdate = models.DateTimeField(default=timezone.now)
    noshares = models.FloatField() #0.1, 0.2, 0.25, 0.5, 0.75, 1.0
    initialcost= models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    maturitydate = models.DateTimeField()
    isActive = models.BooleanField()


#System M:M with bets for keeping up to date with candidates
#enter manually initially or via CSV each day
# racecourseid horseid including outcome as per rpraceday/races

class System(models.Model):

    systemname = models.CharField(max_length=250)
    snapshotid  = models.SmallIntegerField(unique=True)
    description= models.CharField(max_length=250)
    isActive = models.BooleanField(default=True)
    isTurf = models.BooleanField()
    exposure = JSONField()
    query = JSONField()
    funds = models.ManyToManyField(Fund)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('snapshotid',)

#base model variation for Simple, Advanced also Fund, System
class Snapshot(PolymorphicModel):
    #STATS ONLY TIME DEPENDENT
    bfwins = models.SmallIntegerField()
    bfruns = models.SmallIntegerField()
    bfwinpc= models.FloatField()
    expectedwins= models.FloatField()
    a_e = models.FloatField()
    winsr = models.FloatField()
    levelbspprofit= models.DecimalField(max_digits=10, decimal_places=2)
    levelbsprofitpc= models.FloatField()
    a_e_last50 = models.FloatField()
    archie_allruns= models.FloatField()
    expected_last50= models.FloatField()
    archie_last50= models.FloatField()
    last50wins= models.SmallIntegerField()
    last50pc= models.FloatField()
    last50str= models.CharField(max_length=250)
    last28daysruns=  models.SmallIntegerField()
    profit_last50= models.DecimalField(max_digits=10, decimal_places=2)
    longest_losing_streak=models.SmallIntegerField()
    average_losing_streak=models.FloatField()
    average_winning_streak=models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    runners = models.ManyToManyField(Runner)

    class Meta:
        ordering = ('a_e','winsr')

#add year data etc..Fund will only have live data
class SystemSnapshot(Snapshot):
    system = models.ForeignKey(System, related_name='snapshot')
    # exposure= models.ListField() #mongodb

    # query = models.ListField()
    query = models.TextField()

    red_rows_ct = models.SmallIntegerField()
    blue_rows_ct  = models.SmallIntegerField()
    green_rows_ct = models.SmallIntegerField()
    total_rows_ct = models.SmallIntegerField()
    red_rows_pc= models.FloatField()
    blue_rows_pc= models.FloatField()
    green_rows_pc= models.FloatField()
    individualrunners=  models.SmallIntegerField()
    uniquewinners=  models.SmallIntegerField()
    uniquewinnerstorunnerspc= models.FloatField()
    yearstats= JSONField()
    yearcolorcounts= JSONField()
    totalbackyears = models.SmallIntegerField()

class FundSnapshot(Snapshot):
    fund = models.ForeignKey(Fund, related_name='snapshot')
    string_last500 = models.CharField(max_length=250)

#MtoM with SystemSnapshot
#must be convertible to MONGO DB? FOR LOOKUP rpraceday?
class QueryClause(models.Model):
    JOIN_CHOICES = (
    ('AND', 'AND'),('AND(', 'AND('),('OR', 'OR'),
    ('OR(', 'OR('),(')AND', ')AND'),(')OR', ')OR'),
    )
    OPERATOR_CHOICES = (
    ('=', '='),('>', '>'),('>=', '>='),('<', '<'),('<=', '<='),
    ('BETWEEN', 'BETWEEN'),('!=', '!='), ('NOT BETWEEN', 'NOT BETWEEN')
    )
    #SystemSnapshot
    position = models.SmallIntegerField()
    item = models.CharField(max_length=150)
    operator = models.CharField(max_length=15, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=100)
    join = models.CharField(max_length=15, choices=JOIN_CHOICES, default='AND')
    snapshots = models.ManyToManyField(Snapshot)

    def __str__(self):
        return self.position

    class Meta:
        ordering = ('position',)
