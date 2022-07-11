from django.urls import path


from easypays import views


urlpatterns = [
    path('', views.super_easy_pay_view, name='super-easy-pay'),
    
]