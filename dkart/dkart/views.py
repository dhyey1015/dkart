from django.shortcuts import render 
from django.http import HttpResponse
from store.models import Product,ReviewRating

def home(request):
    product = Product.objects.all().filter(is_available = True).order_by('created_date')
    
    #get the reviews
    for product1 in product:
        reviews = ReviewRating.objects.filter(product_id = product1.id, status = True)
    
    context = {
        'products':product,
        'reviews': reviews,
    }

    return render(request,'home.html',context)

def test(request):
    return render(request, "test.html")
    