from django.urls import path

from backoffice import  views



urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('auth/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('base/', views.base, name='base')
    
    ]