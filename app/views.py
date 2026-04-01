from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from .models import Product,Customer,Cart,Wishlist
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import stripe
from django.conf import settings
from django.http import JsonResponse
import json
from django.shortcuts import render
from .models import Payment
from .models import OrderPlaced
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/home.html',locals())
@login_required
def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())
@login_required
def contact(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
           wishitem=len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())


@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
          wishitem=len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,'app/category.html',locals())



@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request,pk):
        product=Product.objects.get(pk=pk)
        wishlist=Wishlist.objects.filter(Q(product=product)& Q(user=request.user))
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))
         wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',locals())


class CustomerRegistrationView(View):
    def get(self , request):
        form=CustomerRegistrationForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
           wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals())


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
          wishitem=len(Wishlist.objects.filter(user=request.user))

        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality , mobile=mobile , city=city, state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request,'app/profile.html',locals())
    
@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request, pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
          wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congrulations Profile Update Sccessfully")
        else:
            messages.warning(request,"Invaild Input Data")
            
        return redirect("address")
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount=amount+value
    totalamount=amount +40
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user=request.user
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product=Wishlist.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals())
    


# class checkout(View):
#     def get(self , request):
#         user=request.user
#         add=Customer.objects.filter(user=user)
#         cart_items=Cart.objects.filter(user=user)
#         famount=0
#         for p in cart_items:
#             value =p.quantity* p.product.discounted_price
#             famount=famount + value
#         totalamount=famount + 40
#         return render(request,'app/checkout.html',locals())



stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(login_required,name='dispatch')
class checkout(View):

    def get(self, request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
          wishitem=len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        famount = 0
        for p in cart_items:
            famount += p.quantity * p.product.discounted_price

        totalamount = famount + 40

        return render(request, 'app/checkout.html', {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount
        })

    def post(self, request):
        # Step 1: Check empty body
        if not request.body:
            return JsonResponse({'error': 'Empty body'}, status=400)

        # Step 2: Parse JSON
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            print("JSON ERROR:", e)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Step 3: Get customer id
        cust_id = data.get("custid")
        if not cust_id:
            return JsonResponse({'error': 'No custid'}, status=400)

        # Step 4: Calculate total amount
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        total_amount = 0
        for p in cart_items:
            total_amount += p.quantity * p.product.discounted_price

        total_amount += 40

        # Step 5: Create Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Cart Payment',
                    },
                    'unit_amount': int(total_amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'http://127.0.0.1:8000/success/?custid={cust_id}',
            cancel_url='http://127.0.0.1:8000/checkout/',
        )

        return JsonResponse({'id': session.id})
    


@login_required
def success(request):
    user = request.user

    cust_id = request.GET.get('custid')
    print("cust_id:", cust_id)

    if not cust_id:
        return HttpResponse("No customer id received")

    try:
        cust_id = int(cust_id)
    except:
        return HttpResponse("cust_id is not number")

    customer = Customer.objects.filter(id=cust_id, user=user).first()

    if not customer:
        return HttpResponse(f"Customer not found: {cust_id}")

    cart = Cart.objects.filter(user=user)

    payment = Payment.objects.create(
        user=user,
        amount=0,
        paid=True
    )

    for c in cart:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity,
            payment=payment
        )

    cart.delete()

    return render(request, "app/success.html")

@login_required
def orders(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())

@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    #print("payment_done: oid=",order_id," pid=",payment_id," cid=",cust_id")
    user=request.user
    #return redirect("orders")
    Customer=Customer.objects.get(id=cust_id)
    #To update payment status and payment_id
    payment=Payment.objects.get(stripe_payment_id=order_id)
    paid=True
    payment.stripe_payment_id=payment_id
    payment.save()
    #To save order  details
    cart=Cart.objects.filter(user=user)
    for c in Cart:
        OrderPlaced(user=user,Customer=Customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")


    
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
            totalamount=amount +40
        data={
            'quantity' : c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)
    

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        else:
            c.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value

        totalamount = amount + 40

        data = {
            'quantity': c.quantity if Cart.objects.filter(id=c.id).exists() else 0,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)







@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
            totalamount=amount +40
        data={
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)


# def plus_wishlist(request):
#     if request.method == 'GET':
#         prod_id=request.method.GET['prod_id']
#         product=Product.objects.get(id=prod_id)
#         user=request.user
#         Wishlist(user=user,product=product).save()
#         data={
#             'message':'Wishlist Added Successfully',
#         }
#         return JsonResponse(data)
    


# def minus_wishlist(request):
#     if request.method == 'GET':
#         prod_id=request.method.GET('prod_id')
#         product=Product.objects.get(id=prod_id)
#         user=request.user
#         Wishlist(user=user,product=product).delete()
#         data={
#             'message':'Wishlist Added Successfully',
#         }
#         return JsonResponse(data)
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'})

        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist.objects.get_or_create(user=user, product=product)

        return JsonResponse({'message': 'Wishlist Added'})
@login_required   
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist.objects.filter(user=user, product=product).delete()

        return JsonResponse({'message': 'Wishlist Removed'})
    
@login_required
def search(request):
    query=request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html',locals())
