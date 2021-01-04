"""nuffle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from nuffleapi.models import players
from django.conf.urls import include
from django.urls import path
from nuffleapi.views import register_user, login_user
from nuffleapi.views.coach import CoachUser
from nuffleapi.views.events import Events
from nuffleapi.views.eventnotes import EventNotes
from nuffleapi.views.eventteams import EventTeams
from nuffleapi.views.leagues import Leagues
from nuffleapi.views.players import Players
from nuffleapi.views.profiles import Profile
from nuffleapi.views.teams import Teams
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'coach', CoachUser, 'coach')
router.register(r'events', Events, 'event')
router.register(r'eventnotes', EventNotes, 'eventnote')
router.register(r'eventteams', EventTeams, 'eventteam')
router.register(r'leagues', Leagues, 'league')
router.register(r'players', Players, 'player')
router.register(r'profile', Profile, 'profiles')
router.register(r'teams', Teams, 'team')
router.register(r'teams/players', Players, 'player')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
