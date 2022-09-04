from django.urls import include, path
from . import views

urlpatterns = [
    path('user/register', views.UserRegisterView.as_view()),
    path('user/login', views.UserLoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('user/<str:restname>/vote', views.UserVoteView.as_view()),
    path('user/logout', views.UserLogoutView.as_view()),
    path('rest/register', views.RestRegisterView.as_view()),
    path('rest/login', views.RestLoginView.as_view()),
    path('rest', views.RestView.as_view()),
    path('rest/<str:restname>/menu/show', views.RestGetMenuView.as_view()),
    path('rest/<str:restname>/stats', views.RestGetStatsView.as_view()),
    path('rest/menu/update', views.RestSetMenuView().as_view()),
    path('rest/logout', views.RestLogoutView.as_view())
]