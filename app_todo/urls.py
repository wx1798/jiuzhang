from django.conf.urls import re_path
from app_todo.views import login, home

urlpatterns = [
    re_path(r'^login/$', login.AuthView.as_view({'post': 'login'})),
    re_path(r'^register/$', login.AuthView.as_view({'post': 'register'})),
    re_path(r'^home/$', home.HomeView.as_view({'post': 'home'})),
    re_path(r'^today/$', home.HomeView.as_view({'post': 'today'})),
    re_path('^update/$', home.HomeView.as_view({'post': 'update'})),
    re_path('^add/$', home.HomeView.as_view({'post': 'add'})),
    re_path('^delete/$', home.HomeView.as_view({'post': "delete"})),
    re_path('^filter/$', home.HomeView.as_view({'post': 'filter'})),
    re_path('^all/$', home.HomeView.as_view({'post': 'all'})),
    re_path('r^find/$', home.HomeView.as_view({'post': 'find'})),
    re_path(r'^send/$', login.AuthView.as_view({'post': 'send'})),
    re_path(r'^init/$', home.HomeView.as_view({'post': 'init'}))
]