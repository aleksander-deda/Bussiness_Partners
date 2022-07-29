from django.shortcuts import render, redirect
from .models import UnderWriter
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from backoffice.models import Member, MemberType, Product, Prelead
from partners.models import Partner
from django.contrib.auth.models import User
from .forms import UnderWriterForm, UserForm
from django.contrib import messages 


# @login_required(login_url='login')
def underwriter_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'underwriters/underwriter_dashboard.html')
    else:
        return redirect('login')
    

class MyProfile( DetailView):
    model = UnderWriter
    context_object_name = 'underwriter'
    template_name = 'underwriters/underwriter_profile.html'
    
    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user).first()
        underwriter = UnderWriter.objects.filter(member_id=member).first()
        return underwriter
    

def profile_update(request, id):
    user = User.objects.get(id=id)
    member = Member.objects.filter(user_id=user).first()
    
    if request.method == 'POST':
        form = UnderWriterForm(request.POST, instance=request.user)
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        if form.is_valid():
            user.username=username
            user.email=email
            user.save()
            
            member.username=username
            member.save()

            return redirect('uw-profile')
        
        else:
            messages.error(request, "Ju lutemi vendosni te dhenat e sakta")
    
    else:
        form = UnderWriterForm()
    
    return render(request, 'underwriters/underwriter_update.html', context={'form': form, 'user': user })


def change_password(request, id):
    user = User.objects.get(id=id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        print("form: ", form)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        print(old_password)
        print(new_password)
        
        if form.is_valid():
            print("hello")
            user.set_password(new_password)
            user.save()
            print(user.password)
            
            return redirect('login')
        
        else:
            messages.error(request, "Fjalëkalimi i ri duhet të jetë i njëjtë me fjalëkalimin e konfirmimit")
    else:
        form = UserForm()
        
    return render(request, 'underwriters/change_password.html', context={'form': form, 'user': user})

    
def preleads_list(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member).first()
    preleads = Prelead.objects.all()
    
    return render (request, 'underwriters/preleads_list.html', {'preleads': preleads})


