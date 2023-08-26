from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from uuid import UUID
from django.contrib import messages
import razorpay
from.models import Product, ProductVariants, Image, Category, Size, ColorVariants
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Cart, CartItem
from django.db.models import Sum
import json


# Create your views here.
def index(request):
    # categories = Category.objects.all()
    # products_by_cat = {}
    # for category in categories:
    #     products = Product.objects.filter(category = category)
    #     print("producs is : ",  products)
    #     products_by_cat[category] = products

    # print(products_by_cat)
    categories = Category.objects.all()
    categories_with_variants = []

    for category in categories:
        products = Product.objects.filter(category = category)
        print("products is : ", products)
        representative_variants = []

        for product in products:
            representative_variant = ProductVariants.objects.filter(product = product).order_by('price').first()
            print('\nrepresentative variants is : ', representative_variant)
            if representative_variant:
                representative_variants.append(representative_variant)
            

        print('representative vairsnt : ', representative_variants)
        if representative_variants:
            categories_with_variants.append({'category':category, 'variants':representative_variants})

    print('categoresi with variatn si s: ',categories_with_variants)
    return render(request, 'app/tem.html',{'categories_with_variants':categories_with_variants})  
    # return render(request, "app/home.html", {'categories':categories, 'products_by_category':products_by_cat})




def product_details(request, slug):
    try:
        variant = get_object_or_404(ProductVariants, slug = slug)
        color = ColorVariants.objects.all()
        sizes = Size.objects.all()
        
        return render(request, 'app/product-details.html', {"variant":variant, 'related_sizes':sizes,'related_colors':color})        
    

    except Exception as e:
        print(e)
    
    return render(request, 'app/home.html')


def add_to_cart(request):
    product_uid = request.POST.get('product_id')
    products = Product.objects.filter(uid = product_uid)     
    variant_redirect = ProductVariants.objects.get(uid = request.POST.get('variant_id'))
    size = request.POST.get('sizes')
    color = request.POST.get('color')    
    print("color is : ",color)    
    print("\n product_uid : ", product_uid)
    print("\n size : ", size)
    product_variant = ProductVariants.objects.filter(product = product_uid, size=size, color = color)
    
    print("product variant is ",product_variant)
    if product_variant.exists():
        if product_variant[0].quantity > 0:
            product_variant = ProductVariants.objects.get(product = product_uid, size=size, color = color)
            if request.user.is_authenticated:
                user_cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                user_cart, created = Cart.objects.get_or_create(session_key=session_key)
    
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, variant = product_variant)
            cart_item.quantity += 1
            cart_item.save()

            messages.success(request, f"{product_variant.product.name} added to cart.")
        else:
            messages.success(request, "out of stock")     
        return redirect('product/'+variant_redirect.slug)     
    else:
        messages.success(request,"not available")
        return redirect('product/'+variant_redirect.slug)
                        
    
            
    


def view_cart(request):        
    discount = 0
    actual_price = 0
    total_actual = 0
    size = 0

    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user = request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        user_cart , created = Cart.objects.get_or_create(session_key = session_key)

    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        action = request.POST.get('action')

        if variant_id and action:
            variant = ProductVariants.objects.get(uid = variant_id)
            cart_item = user_cart.cart_items.filter(variant = variant).first()

            if action == 'add':
                if cart_item:
                    cart_item.quantity +=1
                    print("\n\n\nn\n add is in progress \n\n\n\n\n")
                    cart_item.save()
                else:
                    CartItem.objects.create(cart = user_cart, variant = variant, quantity = 1)
            elif action == 'decrease':
                if cart_item and cart_item.quantity> 1:
                    cart_item.quantity -=1
                    cart_item.save()
            elif action == 'remove':
                if cart_item:
                    cart_item.delete()


    cart_items = user_cart.cart_items.values('variant').annotate(
        total_quantity = Sum('quantity'),
        total_price = Sum('variant__price__price') * Sum('quantity'),
        total_sale_price = Sum('variant__price__sale_price') * Sum('quantity')
    )

    update_cart_items = []

    for item in cart_items:
        variant_uuid = item['variant']
        variant = ProductVariants.objects.get(uid = variant_uuid)
        item['variant'] = variant
        update_cart_items.append(item)                                            
    


    total_price = sum(item['total_price'] for item in cart_items )
    total_sale_price = sum(item['total_sale_price'] for item in cart_items )    
    discount = total_price - total_sale_price
        

    if total_sale_price > 0:        
        client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))        
        data = { "amount": int(total_sale_price*100) , "currency": "INR", "receipt": "order_rcptid_11" }    
        payment = client.order.create(data=data)
        print("\n data is : ", payment)

        return render(request, 'app/cart.html',{'cart_items':update_cart_items, 'total_price':total_price, 'discount':discount, 'total_actual':total_sale_price,'payment':payment })
    return render(request, 'app/cart.html',{'cart_items':update_cart_items, 'total_price':total_price, 'discount':discount, 'total_actual':total_actual })    
    # return render(request, 'app/cart.html')
            

def payment_sucess(request):
    return HttpResponse(request, 'h1 payment sucessx')

@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes)
def sucess(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = CartItem.objects.all()
            cart.delete()
            # Process the received data as needed
            # For example, you can save it to a database
            
            print('i got data')             
            return redirect('app:index')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
