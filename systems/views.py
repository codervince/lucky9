from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Runner, System, Snapshot, Fund, Investment, SystemSnapshot, FundSnapshot, QueryClause
# from django.core.paginator import paginator, EmptyPage, PageNotAnInteger

# def runner_list(request):
#     runners = Fund.object.systems.runners.all()

class WelcomeView(ListView):
    queryset = Fund.objects.all()
    context_object_name = 'funds'
    template_name = 'systems/fund/landing.html'

class FundListView(ListView):
    queryset = Fund.objects.all()
    context_object_name = 'funds'
    template_name = 'systems/fund/list.html'

# def fund_list(request):
#     funds = Fund.objects.all()
#     return render(request, 'systems/fund/list.html', {'funds':funds})

def fund_detail(request, code):
 post = get_object_or_404(Fund, code=code)
 return render(request,
 'blog/post/detail.html',
 {'fund': fund})
# Create your views here.
# { % load bootstrap3 %}
# {%# SImple HTML FORM #%}
# <form action="action_url">
# {% csrf_token %}
