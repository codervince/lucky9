
from django.conf.urls import url
from . import views

urlpatterns = [
# url(r'^$', views.fund_list, name='fund_list'),
url(r'$', views.FundListView.as_view(), name='fund_list'),
url(r'welcome$', views.WelcomeView.as_view(), name='welcome'),
url(r'(?P<fund>[\w]+)/$',
 views.fund_detail,
 name='fund_detail'),


]
