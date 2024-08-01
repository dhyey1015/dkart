from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product,Variation
from .models import Cart, CartItem
from django.http import HttpResponse



# Create your views here.

#get the cart session_id/session_key and if no session_id/session_key  then create session_id/session_key 
def _cart_id(request): 
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def  add_cart(request, product_id, item_id =None):
    product =  Product.objects.get(id = product_id)#get the product
    product_variation = []
    #for product-detail.html
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                #gettion the variations and storing it in product_variation
                variation  = Variation.objects.get(product=product, variation_category__iexact = key,variation_value__iexact=value) 
                product_variation.append(variation)
            except:
                pass
    
    #we are getting cart here
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))#get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id= _cart_id(request)
        )   
    cart.save()
    
    
    
    
    #we are getting cart_item here  
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists: 
        cart_item = CartItem.objects.filter(product = product, cart= cart)
        #existing_variations -> database
        #product current variation product_variation
        #item_id -> database
        
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
        print(ex_var_list)
        
        
        if product_variation in ex_var_list:
            #increase the cart_item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item= CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save() 
            
            
        else:
            item = CartItem.objects.create(product =product,quantity = 1, id=item_id)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
        #cart_item.quantity += 1 #cart_item.queantity means existing cart_item quantity=1
            item.save()
            
            
            
    else:
        cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
        )
        if len(product_variation)>0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.filter(product=product, cart=cart)
    cart_item.delete()
    
    return redirect('cart')
    

        
        
def cart(request,total=0,quanitity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quanitity += cart_item.quantity
            
        tax_rate = 0.2
        tax = total+tax_rate
        grand_total = total + tax
            
    except Cart.DoesNotExist:
        cart_items = []
        tax=0
        grand_total =0
    
    context = {
        
        'total':total,
        'quantity': quanitity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
        
        
    return render(request, "store/cart.html",context)
