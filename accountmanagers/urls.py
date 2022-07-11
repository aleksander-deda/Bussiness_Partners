from django.urls import path
from accountmanagers.views import account_manager_view, partners, add_partner, add_products_to_partners, underwriters


urlpatterns = [
    path('', account_manager_view, name='account-manager'),
    path('partners-list/', partners, name='partners-list'),
    path('underwriters-list/', underwriters, name='underwriters-list'),
    path('add-partners/', add_partner, name='add-partners'),
    path('add-products-to-partners/<int:id>', add_products_to_partners, name='add-products-to-partners'),


]