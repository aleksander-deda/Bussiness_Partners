from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.underwriter_dashboard, name='underwriter'),
    path('my-profile/', views.MyProfile.as_view(), name='my-profile'),
    path('preleads-list/', views.preleads_list, name='prelead-list'),
    
]



