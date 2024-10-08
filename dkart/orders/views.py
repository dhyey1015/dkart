from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem         
from .forms import OrderForm
from store.models import Product
from .models import Order, OrderProduct, Payment
import datetime   
import json    

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import JsonResponse                                                                                                                                                                                                                                                                               

# Create your views here.

def payments(request):
    #store transaction details inside payments model(not working yet)
    # body = json.loads(request.body)
    # order = Order.objects.get(user = request.user, is_ordered = False, order_number=body['orderID'])
    
    # payment = Payment(
    #     user = request.user,
    #     payment_it = body['transID'],
    #     payment_method = body['payment_method'],
    #     amount_paid = order.order_total,
    #     status = body['status'],
    # )
    # payment.save()
    
    # order.payment = payment
    # order.is_ordered = True
    # order.save()
    
    #to store logic body
    #----------------------------------------------------
    
    
    #Move the cart items  to OrderProduct Table
    # cart_item = CartItem.objects.filter(user = request.user)
    
    # for item in cart_item:
    #     orderproduct = OrderProduct()
    #     orderproduct.order_id = order.id
    #    # orderproduct.payment = payment
    #     orderproduct.user_id = request.user.id 
    #     orderproduct.product_id = item.product_id
    #     orderproduct.quantity = item.quantity
    #     orderproduct.product_price = item.product.price
    #     orderproduct.ordered = True
    #     orderproduct.save()
        
    #     cart_item = CartItem.objects.get(id=item.id)
    #     product_variation = cart_item.variations.all()
    #     orderproduct  = OrderProduct.objects.get(id= OrderProduct.id)
    #     orderproduct.variations.set(product_variation)
    #     orderproduct.save()
        
    #     #reduce  the quantity of in stock for sold products
    #     product = Product.objects.get(id = item.product_id)
    #     product.stock -= item.quantity
    #     product.save()
        
        
    # #clear the cart after order is placed
    # CartItem.objects.filter(user = request.user).delete()
    
    # #sending an prder received email to customer
    # mail_subject = "Thank you for your order!"
    #         #sending email body
    # message  = render_to_string('orders/order_recieved_email.html', {
    #         'user':request.user,
    #         'order': order
    # }) 
    # to_email = request.user.email
    # send_email = EmailMessage(mail_subject, message, to = [to_email])
    # send_email.send()
    
    
    # #send order number and transaction id back to sendData method via jsonResponse(this won't work!!!)
    
    # data = {
    #     'order_number': order_number,
    #     'transID': payment.payment_id,
    # }
    # return JsonResponse(data)

     return render(request, 'orders/payments.html')

def place_order(request, total = 0, quantity = 0):
    current_user = request.user
    
    #if the cart count is less or equal to 0 then redirect to store or shop
    
    cart_items = CartItem.objects.filter(user= current_user)
    cart_count = cart_items.count()
    
    
    if cart_count <= 0:
        return redirect('store')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        grand_total = 0
        tax = 0
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
        tax = (2* total)/100
        
        grand_total = total + tax
        
        if form.is_valid():
            
            data = Order()
            
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip  = request.META.get('REMOTE_ADDR')
            data.save()
            
            #to generate order id

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, order_number=order_number)
            
            context= {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
        
def order_complete(request):
    return render(request, 'orders/order_complete.html')
        
        
