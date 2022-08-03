from django.shortcuts import render, redirect
from .models import UnderWriter
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from backoffice.models import Member, MemberType, Product, Prelead
from partners.models import Partner
from django.contrib.auth.models import User
from .forms import UnderWriterForm, UserForm
from django.contrib import messages 
import xlwt
from django.http import HttpResponse


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
    preleads = Prelead.objects.all()
    search_prelead = ""
    filters = {}
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Prelead-Datas.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Data', 'Tipi i Partnerit', 'Partneri', 'Emri', 'Mbiemri', 'Nr.ID', 'Shuma e Aplikuar', 'Shitesi', 'Nr Shitesi', 'Consent BOA', 'Statusi i Aplikimit', 'Statusi i Kontrates', 'Shuma e Aprovuar' ]
    
    if request.method =="POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_status = request.POST.get('status_id')
        search_prelead = request.POST.get('search_prelead')
        print('start_date: ', start_date)
        print('end_date: ', end_date)
        print('selected_status:', selected_status)
        print('search_prelead:', search_prelead)
        
        filters = {
            'start_date': start_date,
            'end_date': end_date,
            'selected_status': selected_status,
        }
        if start_date is not None and end_date is not None and selected_status is not None:
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
                
            preleads = Prelead.objects.filter(created_date__gte=start_date, created_date__lte=end_date, 
            application_status=selected_status).values_list('created_date', 'partner_channel', 'product__partner__name','customer__first_name','customer__last_name','customer__personal_id','applied_amount','seller_name','seller_phone','customer__consent_boa','application_status','contract_status','approved_amount' )
            for prelead in preleads:
                row_num +=1
                for col_num in range(len(prelead)):
                    ws.write(row_num, col_num, prelead[col_num])

            wb.save(response)
            return response
    
    context = {
        'preleads': preleads, 
        'filters': filters,
        'search_prelead': search_prelead,
        }
    
    return render (request, 'underwriters/preleads_list.html', context)



