from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

##MONGO TABLES!

#custom Manager
class LiveManager(models.Manager):
    def get_queryset(self):
        return super(LiveManager,self).get_queryset().filter(runtype='LIVE')


#Pastruns import from CSV# initially then will be updated from RP!

class Runner(models.Model):
    objects = models.Manager()
    live = LiveManager()

    RUNTYPE = (
    ('LIVE', 'LIVE'),
    ('HISTORICAL', 'HISTORICAL'),
    )
    #unique identifiers
    runtype = models.CharField(help_text=_('live_or_historical'), max_length=12, default='HISTORICAL')
    racedate = models.DateField(help_text=_('race date'),)
    racecoursename = models.CharField(help_text=_('racecourse'), max_length=10)
    racecourseid = models.SmallIntegerField(help_text=_('racecouseid'),)
    racename = models.CharField(help_text=_('race name'), max_length=250)
    racetypehorse = models.CharField(help_text=_('entry type horse'),max_length=10)
    racetypeconditions = models.CharField(help_text=_('entry conditions'),max_length=10)
    racetypehs= models.CharField(help_text=_('handicap or stakes'),max_length=10)
    ages = models.CharField(help_text=_('entry type ages'),max_length=10)
    oldraceclass = models.CharField(help_text=_('old raceclass'),max_length=10)
    newraceclass = models.CharField(help_text=_('new raceclass'),max_length=10)
    distance = models.FloatField(help_text=_('distance furlongs'), max_length=10) ##convert
    going = models.CharField(help_text=_('going'),max_length=10) #convert?
    norunners = models.SmallIntegerField(help_text=_('number of runners'),)
    horsename = models.CharField(help_text=_('horse name'),max_length=250)
    sirename = models.CharField(help_text=_('sire name'),max_length=250)
    trainername = models.CharField(help_text=_('trainer'),max_length=250)
    jockeyname = models.CharField(help_text=_('jockey'),max_length=250)
    allowance = models.SmallIntegerField(help_text=_('jockey allowance'),)
    FINALPOS = models.CharField(help_text=_('Final position'),max_length=5)
    lbw = models.FloatField(help_text=_('Beaten by L'),)
    winsp = models.FloatField(help_text=_('final starting price win'),) #may need to be converted
    winsppos = models.SmallIntegerField(help_text=_('rank final starting price'),)
    bfsp = models.DecimalField(help_text=_('Betfair SP win'),max_digits=6, decimal_places=2)
    bfpsp = models.DecimalField(help_text=_('Betfair SP place'),max_digits=6, decimal_places=2)
    fsratingrank = models.SmallIntegerField(help_text=_('FS Rating rank'),)
    fsrating = models.FloatField(help_text=_('FS Rating'),)
    fsraceno = models.CharField(help_text=_('distance'),max_length=250, unique=True)
    draw = models.SmallIntegerField(help_text=_('barrier'),)
    damname = models.CharField(help_text=_('Dam\'s name'),max_length=250)
    damsirename  = models.CharField(help_text=_('Dam\'s sire name'),max_length=250)
    racetime  = models.CharField(help_text=_('Race off time'),max_length=250)
    totalruns =  models.SmallIntegerField(help_text=_('total runs horse'),)
    isPlaced = models.BooleanField(help_text=_('Placed?'),)
    isBFplaced= models.BooleanField(help_text=_('is Placed on Betfair?'),)
    stats = JSONField() #aggregate trainerstats etc

    #snapshotid runnerid--> system_runner table
    class Meta:
        unique_together = ('racedate', 'horsename',)
        ordering = ('-racedate',)

    # timeformrating = models.FloatField(help_text=_('Timeform Rating'),)
    # officialrating= models.FloatField(help_text=_('OR Rating'),)
    # timeformratingrank= models.SmallIntegerField(help_text=_('Timeform Rating rank'),)
    # officialratingrank = models.SmallIntegerField(help_text=_('OR Rating rank'),)



#System M:M with bets for keeping up to date with candidates
#enter manually initially or via CSV each day
# racecourseid horseid including outcome as per rpraceday/races

class System(models.Model):
    ##_systemtype = fs, custom, id
    SYSTEMTYPES = (
    ('tg', 'Trainglot'),
    ('mt', 'Metainvest'),
    ('custom', 'Custom'),
    ('other', 'Other'),
    )
    systemtype = models.CharField(help_text=_('type: '),choices=SYSTEMTYPES, default='tg',max_length=10)
    systemname =  models.CharField(help_text=_('system name'),max_length=10) #2016-T-21T
    snapshotid  = models.SmallIntegerField(unique=True)
    description= models.TextField(help_text=_('rationale'))
    isActive = models.BooleanField(help_text=_('active?'),default=True)
    isTurf = models.BooleanField(help_text=_('turf only?'),default=True)
    exposure = ArrayField(models.CharField(max_length=50), help_text=_('parameters exposed to'),)
    #these are experimental
    query = JSONField(help_text=_('FS query params'),)
    rpquery = JSONField(help_text=_('equivalent RP query params'),)
    ######
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('snapshotid',)

#base model variation for Simple, Advanced also Fund, System
class SystemSnapshot(models.Model):
    snapshotdate = models.DateTimeField()
    system = models.ForeignKey(System, related_name='systemsnapshot')
    runners = models.ManyToManyField(Runner)
    bluerows = JSONField()
    greenrows = JSONField()
    redrows = JSONField()
    yearcolorcounts = JSONField()
    yearstats = JSONField()
    stats = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-snapshotdate',)

class Fund(models.Model):

    def get_absolute_url(self):
        return reverse('systems.fund_detail', args=[self.code])
    CURRENCIES = (
    ('AUD', 'AUD'),
    ('GBP', 'GBP'),
    )
    name = models.CharField(help_text=_('fund name'), max_length=250)
    code = models.CharField( max_length=30, unique=True)
    description = models.TextField(help_text=_('logical reasoning'),)
    isActive = models.BooleanField(help_text=_('active?'),default=True)
    managementfee = models.FloatField(help_text=_('monthly active management fee %'),)
    performancethreshold = models.FloatField(help_text=_('at what rate of return peformance fee starts'),)
    performancefee = models.FloatField(help_text=_('fee for excessive performance'),)
    bailoutfee= models.FloatField(help_text=_('exit at end of month fee %'),)
    bettingratio = models.FloatField(help_text=_('default bet/bank ratio %'),)
    sharespurchased = models.SmallIntegerField(help_text=_('shares you purchased'),)
    initalshareissue = models.SmallIntegerField(help_text=_('total initial share issue'),)
    intialpricepershare = models.DecimalField(max_digits=7, decimal_places=2, help_text=_('initial share price'),)
    currentpricepershare = models.DecimalField(max_digits=7, decimal_places=2, help_text=_('current share price'),)
    currency = models.CharField(max_length=10, choices=CURRENCIES, default='GBP', help_text=_('fund base currency'),)
    openingbank = models.DecimalField(max_digits=7, decimal_places=2, help_text=_('opening bank in currency'),)
    currentbalance = models.DecimalField(max_digits=7, decimal_places=2, help_text=_('current bank %'),)
    liveroi = models.FloatField(help_text=_('current ROI since live'),)
    livesince = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True)
    systems = models.ManyToManyField(System)
    # investors = models.ManyToManyField(
    #     User,
    #     through='Investment',
    #     through_fields=('fund', 'user'),
    # )
    class Meta:
        ordering = ('-liveroi',)


class FundSnapshot(models.Model):
    snapshotdate = models.DateTimeField()
    fund = models.ForeignKey(Fund, related_name='fundsnapshot')
    stats = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-snapshotdate',)
#eg for system:
# {
#     bfwins = models.SmallIntegerField()
#     bfruns = models.SmallIntegerField()
#     winsr = models.FloatField()
#     expectedwins= models.FloatField()
#     a_e = models.FloatField()
#     levelbspprofit= models.DecimalField(max_digits=10, decimal_places=2)
#     levelbsprofitpc= models.FloatField()
#     a_e_last50 = models.FloatField()
#     archie_allruns= models.FloatField()
#     expected_last50= models.FloatField()
#     archie_last50= models.FloatField()
#     last50wins= models.SmallIntegerField()
#     last50pc= models.FloatField()
#     last50str= models.CharField(max_length=250)
#     last28daysruns=  models.SmallIntegerField()
#     profit_last50= models.DecimalField(max_digits=10, decimal_places=2)
#     longest_losing_streak=models.SmallIntegerField()
#     average_losing_streak=models.FloatField()
#     # average_winning_streak=models.FloatField()
# red_rows_ct = models.SmallIntegerField()
# blue_rows_ct  = models.SmallIntegerField()
# green_rows_ct = models.SmallIntegerField()
# total_rows_ct = models.SmallIntegerField()
# red_rows_pc= models.FloatField()
# blue_rows_pc= models.FloatField()
# green_rows_pc= models.FloatField()
# individualrunners=  models.SmallIntegerField()
# uniquewinners=  models.SmallIntegerField()
# uniquewinnerstorunnerspc= models.FloatField()
# yearstats= JSONField()
# yearcolorcounts= JSONField()
# totalbackyears = models.SmallIntegerField()
# }
    #link to table

    #
    # class Meta:
    #     ordering = ('a_e','winsr')

#add year data etc..Fund will only have live data
# class SystemSnapshot(Snapshot):
    # system = models.ForeignKey(System, related_name='snapshot')

    # exposure= models.ListField() #mongodb
    #put this in a data field {}
# {
#     red_rows_ct = models.SmallIntegerField()
#     blue_rows_ct  = models.SmallIntegerField()
#     green_rows_ct = models.SmallIntegerField()
#     total_rows_ct = models.SmallIntegerField()
#     red_rows_pc= models.FloatField()
#     blue_rows_pc= models.FloatField()
#     green_rows_pc= models.FloatField()
#
#     redrows= JSONField()
#     greenrows = JSONField()
#     bluerows =JSONField()
#
#     individualrunners=  models.SmallIntegerField()
#     uniquewinners=  models.SmallIntegerField()
#     uniquewinnerstorunnerspc= models.FloatField()
#     yearstats= JSONField()
#     yearcolorcounts= JSONField()
#     totalbackyears = models.SmallIntegerField()
# }



# a Prodct can be traded on Exchange in Transactions
## How many funds?



### THIS GOES IN SEPARATE CLASS
# class Investment(models.Model):
#     fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     startdate = models.DateTimeField(default=timezone.now)
#     noshares = models.FloatField() #0.1, 0.2, 0.25, 0.5, 0.75, 1.0
#     initialcost= models.FloatField()
#     created = models.DateTimeField(auto_now_add=True)
#     maturitydate = models.DateTimeField()
#     isActive = models.BooleanField()
#MtoM with SystemSnapshot
#must be convertible to MONGO DB? FOR LOOKUP rpraceday?

###THIS WILL NOT BE SEPARATEE !!!! CONDENSE TO LIST uner SYSTEM!

# class QueryClause(models.Model):
#     JOIN_CHOICES = (
#     ('AND', 'AND'),('AND(', 'AND('),('OR', 'OR'),
#     ('OR(', 'OR('),(')AND', ')AND'),(')OR', ')OR'),
#     )
#     OPERATOR_CHOICES = (
#     ('=', '='),('>', '>'),('>=', '>='),('<', '<'),('<=', '<='),
#     ('BETWEEN', 'BETWEEN'),('!=', '!='), ('NOT BETWEEN', 'NOT BETWEEN')
#     )
#     #SystemSnapshot
#     position = models.SmallIntegerField()
#     item = models.CharField(max_length=150)
#     operator = models.CharField(max_length=15, choices=OPERATOR_CHOICES)
#     value = models.CharField(max_length=100)
#     join = models.CharField(max_length=15, choices=JOIN_CHOICES, default='AND')
#     snapshots = models.ManyToManyField(Snapshot)
#
#     def __str__(self):
#         return self.position
#
#     class Meta:
#         ordering = ('position',)
