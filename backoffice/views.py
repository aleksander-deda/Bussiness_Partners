from django.shortcuts import render, redirect
from .models import MemberType, Member
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
       
        
        if user is not None:
            member = Member.objects.filter(user_id=user.id).first()
            member_type_id =  member.member_type_id
            member_type = MemberType.objects.filter(id=member_type_id).first()
            member_type_code = member_type.code

            if user.is_authenticated and member_type_code == "partner":
                auth.login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('partner')
                
            
            if user.is_authenticated and member_type_code == "account_manager":
                auth.login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('account-manager')    
                
                
            if user.is_authenticated and member_type_code == 'underwriter':
                auth.login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('underwriter')
                
                
            if user.is_authenticated and member_type_code == 'super_easy_pay':
                auth.login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('super-easy-pay')
                
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    
    return render(request, 'registration/login.html')


def logout_view(request):
    auth.logout(request)
    return redirect('login')


def base(request):
    
    return render(request, 'main/base.html')

