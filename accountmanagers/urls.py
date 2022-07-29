from django.urls import path
from accountmanagers import views


urlpatterns = [
    path('', views.account_manager_dashboard, name='account-manager'),
    path('my-profile/', views.MyProfile.as_view(), name='am-profile'),
    path('update-profile/<int:id>', views.profile_update, name='update-am-profile'),
    path('change-password/<int:id>', views.change_password, name='change-am-password'),
    path('partners-list/', views.partners, name='partners-list'),
    path('underwriters-list/', views.underwriters, name='underwriters-list'),
    path('add-partners/', views.add_partner, name='add-partners'),
    path('add-products-to-partners/<int:id>', views.add_products_to_partners, name='add-products-to-partners'),


]