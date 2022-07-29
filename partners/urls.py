from django.urls import path
from . import views 

urlpatterns = [
    path('', views.partner_dashboard, name='partner'),
    path('my-profile/', views.MyProfile.as_view(), name='myprofile'),
    path('update-profile/<int:id>', views.profile_update, name='update-partner-profile'),
    path('change-password/<int:id>', views.change_password, name='change-partner-password'),
    path('customers-list/', views.CustomerList.as_view(), name='customers-list'),
    path('preleads-list/', views.preleads_list, name='preleads-list'),
    path('products-list/', views.products_list, name='products-list'),
    # path('customers-list/<int:id>/', views.customers_list, name='customers-list'),
    path('new-application/customer-details', views.new_application_customer_details, name='new-application'),
    path('new-application/calculator', views.new_application_calculator, name='new-application-calculator'),    
]

