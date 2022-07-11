from django.urls import path
from . import views 

urlpatterns = [
    path('', views.partner_dashboard, name='partner'),
    path('my-profile/', views.MyProfile.as_view(), name='my-profile'),
    path('update-profile/', views.ProfileUpdate.as_view(), name='update-profile'),
    path('customers-list/', views.CustomerList.as_view(), name='customers-list'),
    # path('customers-list/<int:id>/', views.customers_list, name='customers-list'),
    path('new-application/customer-details', views.new_application, name='new-application'),
        
]

