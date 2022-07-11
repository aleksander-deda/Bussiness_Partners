from django.shortcuts import render, redirect


# @login_required(login_url='login')
def super_easy_pay_view(request):
    if request.user.is_authenticated:
        return render(request, 'easypays/super_easy_pay_profile.html')
    else:
        return redirect('login')
