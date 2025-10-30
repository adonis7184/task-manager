from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name='devs'
urlpatterns = [
    # developers
    path('developers', views.DeveloperIndexView.as_view(), name='developer_list'),
    path('developers/create', views.DeveloperCreateView.as_view(), name='developer_create'),
    path('developers/<int:pk>', views.DeveloperCreateView.as_view(), name='developer_detail'),

    # teams
    path('teams', views.TeamIndexView.as_view(), name='team_list'),
    path('teams/create', views.create_team, name='team_create'),
    path('teams/<int:pk>', views.edit_team, name='team_detail'),

    # teches
    path('teches', views.TechIndexView.as_view(), name='tech_list'),
    path('teches/create', views.create_tech, name='tech_create'),
    path('teches/<int:pk>', views.edit_tech, name='tech_detail'),

    # testing
    path('auto-escape', views.autoescape, name='auto_escape'),

    # auth
    # path('login', views.MyLogin.as_view(), name='login'),
    # path('register', views.MyRegister.as_view(), name='register'),
    # path('logout', views.MyLogout.as_view(next_page='/devs/login'), name='logout')
]