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


customer = None
partner = None
prelead = None


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
    
    
    
class ProfileUpdate(UpdateView):
    model = Partner
    form_class = PartnerForm
    user_form_class = UserForm
   
    # context_object_name = 'partner'
    success_url = reverse_lazy('my-profile')

    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user.id).first()
        partner = Partner.objects.filter(member_id=member.id).first()
        
        return partner
    
    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)        
        context['users'] = User.objects.all()
        context['member'] = context['users'].filter(username=self.request.user.username).first()
       
        # context['user'] = context['users'].filter(id=self.request.user.id, is_active=True)
        
        # context['users'] = User.objects.get(id=self.request.user.id)
        
        
        return context


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



def new_application_calculator(request):
    today = datetime.datetime.strftime(datetime.datetime.today().now(), '%Y-%m-%d %H:%M:%S')
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member, is_active=True).first()
    products = PartnerProduct.objects.filter(partner_id=partner.id, start_date__lte=today, is_active=True)
    datas = {}
    context={}
    
    if request.method == 'POST':
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')
        print(seller_name)
        print(seller_phone)
        selected_product = request.POST.get('product_id')
        applied_amount = float(request.POST.get('applied_amount'))
        loan_term = float(request.POST.get('loan_term'))
        loan_confirm = request.POST.get('loan_confirm')
        print(selected_product)
        print(loan_confirm)
        
        datas = {           
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            # 'loan_month': loan_month,
            'applied_amount': applied_amount,
            'loan_term': loan_term,
        }
        print('datas: ',datas) 
        
        
        
        if seller_name is not None and seller_phone is not None and selected_product is not None and applied_amount is not None and loan_term is not None:
            loan_config = LoanConfig.objects.filter(product_id=selected_product, min_loan_term__lte=loan_term, max_loan_term__gte=loan_term).first()
            product = PartnerProduct.objects.filter(partner_id=partner.id, product_id=selected_product, is_active=True).first()
            print("loan_config: ", loan_config)
                    
            if loan_config is not None:
                interest = float(loan_config.customer_interest)
                fee = float(loan_config.partner_fee_without_bonus)
                total = float(applied_amount + applied_amount*interest + applied_amount*fee)
                print('applied_amount: ', applied_amount)
                print('total: ' ,total)
                
                loan_month = float(total/loan_term)
                print('loan_term: ', loan_term)
                print("loan_month: ",loan_month)
                           
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
                    
                
                else:
                     return redirect('new-application-calculator')
            else:
                messages.error(request, 'Produkti nuk u gjet!')
            
            return redirect('preleads-list')
            messages.success(request, 'Aplikimi per klientin u krye me sukses')
    context = {
            'products': products,
            'datas': datas,
        }
    print('datas1: ',context['datas'])
    
    
                
    return render (request, 'partners/new_application_calculator.html', context)
    
