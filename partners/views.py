from hashlib import new
from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Customer, Partner, PartnerProduct, LoanConfig
from backoffice.models import Prelead, Member, Product
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from .forms import PartnerForm, UserForm
import datetime
from django.contrib import messages


# @login_required(login_url='login')
def partner_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'partners/partner_dashboard.html')
    else:
        return redirect('login')
    


class MyProfile( DetailView):
    model = Partner
    context_object_name = 'partner'
    template_name = 'partners/partner_profile.html'
    
    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user).first()
        partner = Partner.objects.filter(member_id=member).first()
        return partner
    

def change_password(request, id):
    user = User.objects.get(id=id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member).first()
    
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

    return render(request, 'partners/change_password.html', context={'form': form, 'user': user})



def profile_update(request, id):
    user = User.objects.get(id=id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member).first()
    
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=request.user)
        username = request.POST.get('username')
        email = request.POST.get('email')
        nr_tel = request.POST.get('nr_tel')

        if form.is_valid():
            user.username=username
            user.email=email
            user.save()
            
            member.username=username
            member.save()

            partner.nr_tel=nr_tel
            partner.save()
            return redirect('partner-profile')
        
        else:
            messages.error(request, "Ju lutemi vendosni te dhenat e sakta")
    
    else:
        form = PartnerForm()
    
    return render(request, 'partners/partner_update.html', context={'form': form, 'user': user,'partner': partner })



class CustomerList( ListView):
    model = Customer
    context_object_name = 'customers'               
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user).first()
        partner = Partner.objects.filter(member_id=member).first()
        context['customers'] = context['customers'].filter(partner_id=partner, is_active=True)
        # context['count'] = context['customers'].filter( is_active=True).count()
        
        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['tasks'] = context['tasks'].filter(
        #         title__startswith=search_input)
        # context['search_input'] = search_input
        
        return context      
    
    
    
def preleads_list(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member, is_active=True).first()
    preleads = Prelead.objects.filter(product__partner=partner, is_active=True)
    
    return render (request, 'partners/prelead_list.html', {'preleads': preleads})



def products_list(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member, is_active=True).first()
    products = PartnerProduct.objects.filter(partner=partner, is_active=True)
    
    
    return render (request, 'partners/products_list.html', {'products': products})
   
   

def new_application_customer_details(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member, is_active=True).first()
    print('partner ', partner)
    # # partner_products = PartnerProduct.objects.filter(partner_id=2, is_active=True).first()
    # partner_products = PartnerProduct.objects.filter(partner_id=partner.id, is_active=True).first()
    # products = PartnerProduct.objects.filter(partner_id=partner.id, is_active=True)
    # print('partner_products ', partner_products)
    context = {}
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        personal_id = request.POST.get('personal_id')
        id_card_doc = request.FILES['id_card_doc']
        klauzole_doc = request.FILES['klauzole_doc']
        birthdate = request.POST.get('birthdate')
        mobile = request.POST.get('mobile')
        print(first_name)
        
        
        customer_details = {
            'first_name': first_name,
            'last_name': last_name,
            'personal_id': personal_id,
            'id_card_doc': id_card_doc,
            'klauzole_doc': klauzole_doc,
            'birthdate': birthdate,
            'mobile': mobile,
        
        }
        context={
            'customer':customer_details,
        }
        
        if first_name is not None and last_name is not None and personal_id is not None and id_card_doc is not None and klauzole_doc is not None and birthdate is not None and mobile is not None:
            customer = Customer(partner=partner, first_name=first_name, last_name=last_name, personal_id=personal_id,
                                    id_card_doc=id_card_doc, klauzole_doc=klauzole_doc, birthdate=birthdate, mobile=mobile)
            
            request.session['customer'] = customer
            # request.session['customer'].save()
            print('session: ',request.session['customer'])
            print('customer object: ', customer)
        
        return redirect('new-application-calculator')
    return render(request, 'partners/new_application_customer_details.html', context)



def calculating_product_results(partner_fee_without_bonus,partner_fee_with_bonus,customer_interest, application_commission,bonus,applied_amount,loan_term, has_bonus):
    calculator = {}
    
    if has_bonus is None:
    
        total = float(applied_amount + applied_amount * customer_interest + applied_amount * partner_fee_without_bonus + applied_amount * application_commission)
        loan_month = float(total/loan_term)
        print("Totali pa bonus: ", total)
        print("Monthly_loan pa bonus: ", loan_month)

    else:
        total = float(applied_amount + applied_amount * customer_interest + applied_amount * partner_fee_with_bonus + applied_amount * bonus + applied_amount * application_commission)
        loan_month = float(total/loan_term)

        print("Totali me bonus: ", total)
        print("Monthly_loan me bonus: ", loan_month)
    
    
    calculator = { "total": total,"loan_month": loan_month}
    print("calculator: ", calculator)
    
    return calculator 



def new_application_calculator(request):
    today = datetime.datetime.strftime(datetime.datetime.today().now(), '%Y-%m-%d %H:%M:%S')
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member, is_active=True).first()
    products = PartnerProduct.objects.filter(partner_id=partner.id, start_date__lte=today, is_active=True)
    datas = {}
    result = {}
    
    if request.method == 'POST':
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')
        selected_product = request.POST.get('product_id')
        applied_amount = float(request.POST.get('applied_amount'))
        loan_term = float(request.POST.get('loan_term'))
        loan_confirm = request.POST.get('loan_confirm')
        has_bonus = request.POST.get('has_bonus')

        print("has_bonus: ", has_bonus)
        
        if seller_name is not None and seller_phone is not None and selected_product is not None and applied_amount is not None and loan_term is not None:
            loan_config = LoanConfig.objects.filter(product_id=selected_product, min_loan_term__lte=loan_term, max_loan_term__gte=loan_term).first()
            product = PartnerProduct.objects.filter(partner_id=partner.id, product_id=selected_product, is_active=True).first()
            print("loan_config: ", loan_config)
                    
            if loan_config is not None:
                result = calculating_product_results(loan_config.partner_fee_without_bonus,loan_config.partner_fee_with_bonus,loan_config.customer_interest, 
                            loan_config.application_commission,loan_config.bonus,applied_amount,loan_term, has_bonus)
                
                
                datas = {           
                'seller_name': seller_name,
                'seller_phone': seller_phone,
                'selected_product': selected_product,
                'applied_amount': applied_amount,
                'loan_term': loan_term,
                'has_bonus': has_bonus,
                
                        }
                print('datas: ',datas)
                           
                if loan_confirm is not None:
                    print('Hello World!!!!')
                    customer_obj = request.session.get('customer')
                    print(customer_obj)
                    customer_obj.save()
                    print("final customer: ", customer_obj)
                    
                    prelead = Prelead(customer=customer_obj, product=product, 
                                    seller_name=seller_name,seller_phone=seller_phone,applied_amount=applied_amount,
                                    loan_term=loan_term)
                    
                    print('Prelead: ', prelead)    
                    prelead.save()   
                
                    return redirect('preleads-list')   
            
            else:
                messages.error(request, 'Produkti me keto te dhena nuk u gjet!')
              
        # else:
        #     messages.success(request, 'Aplikimi per klientin u krye me sukses')

        print("selected_produc before context: ", selected_product)

    context = {
        'products': products,
        'datas': datas,
        'results': result  
        }
    
    print('datas1: ',context['datas'])

    return render (request, 'partners/new_application_calculator.html', context)
    
