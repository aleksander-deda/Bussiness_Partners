from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.underwriter_view, name='underwriter'),
    
]



