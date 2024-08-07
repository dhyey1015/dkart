from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse

#verification of email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def register(request):
    
    
    if request.method == 'POST':
        
        #try:
          #  data = json.loads(request.body)
          #  first_name = data.get('first_name', None)
          #  last_name = data.get('last_name', None)
          #  email = data.get('email', None)
           # phone_number = data.get('phone_number', None)
           # password = data.get('password', None)
           # username = email.split("@")[0]
            
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name = first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()
            #USER ACTIVATION 
            current_site =  get_current_site(request)
            mail_subject = "Please activate your account"
            #sending email body
            message  = render_to_string('accounts/account_verification.html', {
                    'user':user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
            }) 
            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            
            send_email.send()
            
            messages.success(request, 'Thank you fro registering with us. We have  send you an verification email you your email address.please verify it')
        return redirect('/accounts/login/?command=verification&email='+email)
            #return JsonResponse({
             #   'success': True,
             #   'message': "You are now Registered",
             #   'user': {
             #       'email': email,
              #      'username': username
              #  }
           # })
            
        #except json.JSONDecodeError:
           # return JsonResponse({
              #  'success': False,
            #    'message': "Invalid JSON"
           # }, status=400)
        
    #else: 
        #return JsonResponse({
         #   'success': False,
          #  'message': "Invalid something"
       # }, status=401) 
        
            
    form =  RegistrationForm() 
    context= {
        'form':form,
    }
    return render(request, 'accounts/register.html', context) #<_---------)context) here

@csrf_exempt
def login(request):

    if request.method == 'POST':
        #try:
        #data = json.loads(request.body)
        #email = data.get('email', None)
        #password = data.get('password', None)
        email = request.POST['email']
        password = request.POST['password']
            
        user = auth.authenticate(email=email, password=password)
            
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")  
            return redirect('dashboard')
            
            # return JsonResponse({
                #  'success': True,
                #  'message': "You are now logged in",
                #  'user': {
                #       'email': user.email
                    #}
            #})
                   
            
        else: 
            messages.error(request, "Invalid login credentials")
            return redirect('login')
        
    return render(request, 'accounts/login.html')
                
            #return JsonResponse({
                #  'success': False,
                #  'message': "Invalid login credentials"
            #}, status=401)
               
            
            
        #except json.JSONDecodeError:
            #return JsonResponse({
               # 'success': False,
                #'message': "Invalid JSON"
           # }, status=400)
        
    #return JsonResponse({
      #  'success': False,
     #   'message': "Invalid request method"
    #}, status=400)       
    

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')
    
    
def activate(request,uidb64,token):
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! your account is activated")
        return redirect('login')
    else: 
        messages.error(request, "Invalid activation link")
        return redirect('register')
    
@login_required(login_url = 'login')  
def dashboard (request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword (request):
    
    if request.method == 'POST':
        email = request.POST['email']
        
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #reset password email send here
            
            current_site =  get_current_site(request)
            mail_subject = "Reset your password"
            #sending email body
            message  = render_to_string('accounts/reset_password_email.html', {
                    'user':user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }) 
            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
            
            messages.success(request,'Password reset link has been send to your email address')
            return redirect('login')
            
            
            
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
            
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64,token):
    
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error('This link is expired')
        return redirect('login')
    
def resetPassword(request):
    
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        
        else:
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
        
    else: 
        return render(request, 'accounts/resetPassword.html')
    
