from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import HttpResponseRedirect, JsonResponse
from .models import product,history
from builtins import classmethod
from django.contrib import messages
#from twilio.rest import Client
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from mainapp.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
import time 
from django.utils.html import strip_tags
#import pdfkit
from django.template.loader import render_to_string, get_template
import pandas as pd
import os
#import pdfkit as pdf
import random
from string import ascii_uppercase
import string


 
 # created in step 4

# Create your views here.
# page redirections here


def home(request):
    if request.method == 'GET':
        data = product.objects.all()[:10]
    
        return render(request, 'home.html',{'data':data})

def profile_view(request):
    return render(request,'profile.html')


def category(request):
    if request.method == 'GET':
        data = product.objects.all()
        dairy = product.objects.filter(category='dairy')
        vege = product.objects.filter(category='vegetables')
        grocery = product.objects.filter(category='grocery')

        cart = Cart(request)
        cartpid = []

        for key, value in request.session['cart'].items():
            cartpid.append(value['product_id'])
            x = value['product_id']

        return render(request, 'category.html', {'data': data, 'dairy': dairy, 'vege': vege, 'grocery': grocery,
                                                 'errorl': 'Please Login TO Purchase', 'cartpid': cartpid})
    else:
        print("No Data Found ")


def search(request):
    return render(request, 'search.html')


def registration_page(request):
    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')
    

def cart_page(request):
    
    return render(request,'cart.html')
def forgotpage(request):
    return render(request,'forgotpassword.html')
    
# user authentication


def save_data(request):
    if request.method == 'POST':
        user_name = request.POST['first_name']
        # last_name = request.POST['Last_name']
        # username=first_name+last_name
        number = request.POST['mobile']
        username = request.POST['email']
        address = request.POST['address']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        # print(first_name,last_name,number,email,address,password1)
        if password1 == password2:
            # if User.objects.filter(email=user_name).exists():
            if User.objects.filter(username=username).exists():
                # print("username is already exist")
                return render(request, 'register.html', {'errore': 'Email is already taken'})

            else:
                # return test(request, username, email, password1)
                user = User.objects.create_user(
                    username=username, first_name=address, last_name=number, email=user_name, password=password1)

                user.save()
                auth.login(request, user)
                return render(request, 'home.html')
               

        else:
            # print("password is not matching")
            return render(request, 'register.html', {'errorp': 'Please Check Your Password'})


def Login(request):

    username = request.POST['email_login']
    password = request.POST['password_1']
    # print(email_log,password_log)
    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        # print("user logged in successfully")
        return redirect( '/' )
    else:
        # print("invalid credentials")
       return render(request, 'login.html', {'error': 'Email or Password is incorrect'})
       

def Logout(request):
    logout(request)
    return redirect('/')

# forgot password
def forgot(request):

    if request.method =='POST':
        username = request.POST['email_forgot']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
       
        if  User.objects.filter(username=username).exists():
            if password1 == password2:
                u = User.objects.get(username=username)
                u.set_password(password1)

                u.save()
                return render(request,'login.html')
        
            else:
                # print("password is not matching")
                return render(request, 'forgotpassword.html', {'errorp': 'Please Check Your Password'})
        else:
            return HttpResponse("! Sorry we are unable to process your request because your Email does not exit please go back and try again..! ") 
    else:
        print("something went wrong")   


# Reset Password 
# def reset_password(request):
#     un = request.GET["username"]
#     try:
#         user = get_object_or_404(User, username=un)
#         otp = random.randint(1000, 9999)
#         msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(
#             user.username, otp)
#         try:
#             email = EmailMessage("Account Verification", msz, to=[user.email])
#             email.send()
#             return JsonResponse({"status": "sent", "email": user.email, "rotp": otp})
#         except:
#             return JsonResponse({"status": "error", "email": user.email})
#     except:
#         return JsonResponse({"status": "failed"})
#  cart


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    data = product.objects.get(id=id)
    cart.add(product=data)

    return redirect('/categories')

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    data = product.objects.get(id=id)
    cart.remove(product=data)
   
    return redirect('/cart/')


@login_required(login_url="/users/login")
def cart_total_amount(request):
	if request.user.is_authenticated:
        
		cart = Cart(request)
		total_bill = 0.0
		for key, value in request.session['cart'].items():
			total_bill = total_bill + (float(value['price']) * value['quantity'])
            
		return {'cart_total_amount': total_bill}
	else:
		return {'cart_total_amount': 0}


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    data = product.objects.get(id=id)
    cart.add(product=data)
   
    return redirect("/cart/")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    data= product.objects.get(id=id)
    for key, value in request.session['cart'].items():
        if key == str(data.id):

            value['quantity'] = value['quantity'] - 1
            if(value['quantity']< 1 ):
                return redirect('/cart/')
            cart.save()
            break
        else:
            print("Something Wrong")
    
    return redirect("/cart/")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/cart/")



# invoice bill for purchased order

@login_required(login_url="/users/login")
def invoice(request):
    if request.user.is_authenticated:
        customer_name=request.user.email
        customer_email=request.user.username
        customer_number=request.user.last_name
        customer_address =  request.user.first_name
       
        cart = Cart(request)
       
        named_tuple = time.localtime()  # get struct_time
        orderplaced_time = time.strftime("%m-%d-%Y, %H:%M:%S", named_tuple)
        
        summery_list = {}
        total_bill = 0.0
        for key, value in request.session['cart'].items():
            product_name=value['name']
            summery_list['product_name'] = product_name
            # print(product_name)
            product_price= value['price']
            summery_list['product_price'] = product_price

            # print(product_price)
            product_quantity= value['quantity']
            summery_list['product_quantity'] = product_quantity
            # print(product_quantity)
            total_bill = total_bill + (float(value['price']) * value['quantity'])
            summery_list['total_bill'] = total_bill
            total_amount= total_bill
            # print(total_amount)
            # summery = [customer_name, customer_email, customer_number, product_name, product_quantity, product_quantity, total_amount]
            # summery1=[summery]
        # for data in summery_list:
        #     data= data
        #     p_name=summery_list['product_name']
        #     p_price =summery_list['product_price']
        #     p_quantity=summery_list['product_quantity']
        #     p_total=summery_list['total_bill']
    elif request.GET.get('mainbtn') or request.GET.get('probtn'):
        print("button clicked")
    else:
        print("user not found")
    
 

    return render(request, 'orderstep4.html', {'orderplaced_time':orderplaced_time})
# pdf html


# order placed email from user to admi
@login_required(login_url="/users/login")
def mail_confirm(request):
    if request.user.is_authenticated:
        customer_name = request.user.email
        customer_email = request.user.username
        customer_number = request.user.last_name
        customer_address = request.user.first_name
        
        named_tuple = time.localtime()  # get struct_time
        orderplaced_time = time.strftime("%m-%d-%Y, %H:%M:%S", named_tuple)

        cart = Cart(request)
        invoiceid = []
        product_names = []
        product_quantity = []
        product_price = []
        product_bill = []
        product_Grand = []
        total_bill = 0.0
        p_names = ""

#         # random = ''.join([random.choice(ascii_uppercase+ string.digits) for n in range(10)])

        invoice_id = ''.join([random.choice(ascii_uppercase
                                        + string.digits) for n in range(10)])+str(request.user.id)
        uniqid=invoice_id
        invoiceid.append(uniqid)
        for key, value in request.session['cart'].items():

            # product_name = value['name']
            # summery_list.append(product_name)

            # product_price = value['price']
            # # summery_list.append(product_price)

            # product_quantity = value['quantity']
            # # summery_list.append(product_quantity)
            total = (float(value['price']) * value['quantity'])
            total_bill = total_bill + \
                (float(value['price']) * value['quantity'])
            # summery_list.append(total_bill)
            total_amount = total_bill

            name = value['name']
            p_names = p_names+name
            product_names.append(name)
            quantity = value['quantity']
            product_quantity.append(quantity)
            price = value['price']
            product_price.append(price)
            product_bill.append(total)
            product_Grand.append(total_bill)

        df = pd.DataFrame(list(zip( product_names, product_quantity, product_price, product_bill, product_Grand)),
                          columns=[ 'Name', 'Quantity', 'Price', 'Total', 'Grand Total'])
        # df = pd.DataFrame(filtered_data)
        file = df.to_html('invoice.html')
        print(df)
        h = history()
        h.invoice_id = invoice_id
        h.p_name = p_names
        h.totalamount = total_bill
        h.customer_id = request.user.id
        h.custmer_email = request.user.username
        

        subject = 'Order Confirmed'
        recipient_list = ['satyaambati5@gmail.com',
                          'suhanashunnu123@gmail.com', 'sowmyajakkampudi2000@gmail.com']

        msg = EmailMessage(subject, "\n INVOICE ID:"+invoice_id + "\n NAME:" + customer_name + "\nEMAIL:" + customer_email + "\nMOBILE NUMBER:" + customer_number
        + "\nADDRESS:" +customer_address + "\nTIME:" +orderplaced_time +"\nSUMMERY:",'mailb2331@gmail.com', recipient_list,)
        msg.attach_file(
            'invoice.html', 'text/html')
        msg.send()
        h.save()
        # cart_clear(request)
    else:
        print("user not found")
    
    return render(request, 'orderstep4.html', {'invid': invoice_id, 'orderplaced_time': orderplaced_time})


'''
@login_required(login_url="/users/login")
def mail_confirm(request):

    if request.user.is_authenticated:
        customer_name = request.user.email
        customer_email = request.user.username
        customer_number = request.user.last_name
        customer_address = request.user.first_name
        orderplaced_time = asctime()
        cart = Cart(request)
        invoiceid =[]
        product_names = []
        product_quantity = []
        print(product_quantity,product_names)
        product_price = []
        product_bill =[]
        product_Grand=[]
        total_bill = 0.0
        p_names=""
        
        # random = ''.join([random.choice(ascii_uppercase+ string.digits) for n in range(10)])

        invoice_id = ''.join([random.choice(ascii_uppercase
                                        + string.digits) for n in range(10)])+str(request.user.id)
        uniqid=invoice_id
        invoiceid.append(uniqid)
        for key, value in request.session['cart'].items():
           
            # product_name = value['name']
            # summery_list.append(product_name) 
        
            # product_price = value['price']
            # # summery_list.append(product_price) 


            # product_quantity = value['quantity']
            # # summery_list.append(product_quantity) 
            total = (float(value['price']) * value['quantity'])
            total_bill = total_bill + (float(value['price']) * value['quantity'])
            # summery_list.append(total_bill) 
            total_amount = total_bill
                
            name = value['name']
            p_names =p_names+name
            product_names.append(name)
            print(product_names)
            quantity = value['quantity']
            product_quantity.append(quantity)
            price = value['price']
            product_price.append(price)
            product_bill.append(total)
            product_Grand.append(total_bill)
        # h = history()
        # h.invoice_id = invoice_id
        # h.p_name = p_names
        # h.totalamount = total_bill
        # h.customer_id = request.user.id
        # h.custmer_email = request.user.username
        # h.save()
            
        df = pd.DataFrame(list(zip(invoiceid,product_names, product_quantity, product_price,product_bill,product_Grand)),
                        columns=['INVOICE_ID','Name', 'Quantity', 'Price' ,'Total','Grand Total'])
        # df = pd.DataFrame(filtered_data)
        print(df)
        file= df.to_html ('invoice.html')
        print(file)
        df.head()
        
        print(df)

        subject = 'Order Confirmed'
        recipient_list = ['satyaambati5@gmail.com','suhanashunnu123@gmail.com','sowmyajakkampudi2000@gmail.com']
        

        msg = EmailMessage(subject,"\n INVOICE ID:"+invoice_id+ "\n NAME:" + customer_name + "\nEMAIL:" + customer_email + "\nMOBILE NUMBER:" + customer_number
        + "\nADDRESS:" +customer_address + "\nTIME:" +orderplaced_time +"\nSUMMERY:",'mailb2331@gmail.com', recipient_list,)
        msg.attach_file( 'invoice.html', 'text/html')
       
        msg.send()
       
        # cart_clear(request)
    else:
        print("user not found")        
    

    orderplaced_time = asctime()
    return render(request, 'orderstep4.html', {'invid': invoice_id, 'orderplaced_time': orderplaced_time})
  ''' 

@login_required(login_url="/users/login")
def orderstep1(request):
    return render(request,'orderstep1.html')


@login_required(login_url="/users/login")
def orderstep2(request):
    # if request.method == 'POST':
    #     invid = request.POST['email_login']

    return render(request, 'orderstep2.html')


@login_required(login_url="/users/login")
def order_history(request):
    hist = history.objects.filter(customer_id=request.user.id)
    customer_name = request.user.email
    customer_email = request.user.username
    customer_number = request.user.last_name
    customer_address = request.user.first_name
    named_tuple = time.localtime()  # get struct_time
    orderCanceled_time = time.strftime("%m-%d-%Y, %H:%M:%S", named_tuple)

    invid = ""
    
    if(request.GET.get('mybtn')):
        invid=invid+request.GET.get('invoice_id')
        print(invid)
        # print("test is success")

        if history.objects.filter(invoice_id=invid).exists():
            
            data_row=history.objects.get(invoice_id=invid)
            print(data_row)
            # print("id is exist")
            subject = "Order Canceled by::"+customer_name
            recipient_list = ['satyaambati5@gmail.com',
                            'suhanashunnu123@gmail.com', 'sowmyajakkampudi2000@gmail.com']

            msg_cancel_order = EmailMessage(subject, "\n INVOICE ID:"+invid + "\n NAME:" + customer_name + "\nEMAIL:" + customer_email + "\nMOBILE NUMBER:" + customer_number
                                            + "\nADDRESS:" + customer_address + "\nTIME:" + orderCanceled_time + "\nSUMMERY:", 'mailb2331@gmail.com', recipient_list,)

            msg_cancel_order.send()
            data_row.delete()
           

    return render(request, 'history.html', {'hist': hist})
    
# @login_required(login_url="/users/login")
# def cancelorder(request):
#     if(request.GET.get('mybtn')):
#         print("test success")
#     return HttpResponse("yourder canceled",)

