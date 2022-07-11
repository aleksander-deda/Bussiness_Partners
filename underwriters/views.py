from django.shortcuts import render, redirect


# @login_required(login_url='login')
def underwriter_view(request):
    if request.user.is_authenticated:
        return render(request, 'underwriters/underwriter_profile.html')
    else:
        return redirect('login')