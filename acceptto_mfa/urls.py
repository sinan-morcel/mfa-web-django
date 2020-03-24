from django.urls import path

from . import views

app_name = 'acceptto_mfa'
urlpatterns = [
    path('', views.index_login_view, name='index_login'),
    path('login/', views.index_login_view, name='index_login'),
    path('wait/', views.wait_view, name='wait'),
    path('decision/<str:side>/<str:username>/<str:channel>', views.auth_decision_view, name='auth_decision'),
    path('dashboard/<str:username>/', views.dashboard_view, name='dashboard'),
]
