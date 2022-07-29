from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.underwriter_dashboard, name='underwriter'),
    path('my-profile/', views.MyProfile.as_view(), name='uw-profile'),
    path('update-profile/<int:id>', views.profile_update, name='update-uw-profile'),
    path('change-password/<int:id>', views.change_password, name='change-uw-password'),
    path('preleads-list/', views.preleads_list, name='prelead-list'),
    
]



