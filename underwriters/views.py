from django.shortcuts import render, redirect
from .models import UnderWriter
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from backoffice.models import Member, MemberType, Product, Prelead
from partners.models import Partner
from django.contrib.auth.models import User


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
    
    
def preleads_list(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member).first()
    preleads = Prelead.objects.all()
    
    return render (request, 'underwriters/preleads_list.html', {'preleads': preleads})


