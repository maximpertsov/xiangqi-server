"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from xiangqi import views

urlpatterns = [
    path("api/token/obtain", obtain_jwt_token, name="token_create"),
    path(
        "api/token/refresh",
        views.RefreshJSONWebTokenFromCookie.as_view(),
        name="token_refresh",
    ),
    path("api/position", views.PositionView.as_view()),
    path("api/starting-position", views.StartingPositionView.as_view()),
    path("api/player/<str:username>/games", views.GameListView.as_view()),
    path("api/game/events", views.GameEventView.as_view()),
    path("api/game/requests", views.GameRequestView.as_view()),
    path("api/game/<str:slug>/poll", views.PollView.as_view()),
    path("api/game/<str:slug>", views.GameView.as_view()),
    path("admin/", admin.site.urls),
]
