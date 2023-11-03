from django.shortcuts import render, redirect
from .models import Product, Contact, Order, Profile
from math import ceil
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import joblib
from django.contrib.auth import logout
import pickle
# Create your views here.


def show_recommendations(product):
    model = pickle.load(open("product_recommendation_model.sav", "rb"))

 
def index(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))

        allProds.append([prod, range(1, nslides), nslides])
    username = ""
    if request.user.is_authenticated:
        username = request.session.get('name', 'name')
    
    ordered_pro_history = []
    # user_history = Profile.objects.filter(username = request.user)

    # for i in user_history:
    #     ordered_pro = Product.objects.filter(id=i)
    #     ordered_pro_history.append(ordered_pro)

    print(ordered_pro_history)

    params = {'allProds': allProds, 'username': username, 'ordered_pro_history': ordered_pro_history}
    
    return render(request, 'shop/index.html', params)


def categorywise(request, category):
    print(category)
    prod = Product.objects.filter(category=category)
    print(prod)
    n = len(prod)
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    allProds = []
    allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds}
    return render(request, 'shop/categorywise.html', params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        print(request)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contactform = Contact(name=name , email=email, phone=phone, desc=desc)
        contactform.save()
    return render(request, 'shop/contact.html')

def search(request):
    query = request.GET.get('search')
    print(query.lower())
    pro_names = Product.objects.values('product_name')
    allProds = []

    for items in pro_names:
        if query.lower() in items['product_name'].lower():
            prod = Product.objects.filter(product_name=items['product_name'])
            n = len(prod)
            nslides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nslides), nslides])
    
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def productview(request, myid):
    product = Product.objects.filter(id=myid)
    print(product)
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        if request.method == "POST":

            name = request.POST.get('name', '')
            # print(name)
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')
            address2 = request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            order = Order(product_id = myid,product_desc = "", user_id = user_id, name=name, email=email, phone=phone, address=address, address2=address2, city=city,
                          state=state)
            order.save()
            thank = True
            id = order.ord_id
            
            return render(request, 'shop/productview.html', {'thank': thank, 'id': id})
    else:
        return redirect("shop:login")
        if user is not None:
            login(request, user)
            return redirect("shop:product")
    return render(request, 'shop/   productview.html', {'product':product[0]})

def checkout(request):
    return render(request, 'shop/checkout.html')

def yourcart(request):

    return render(request, 'shop/yourcart.html')

# register = template.Library()

# @register.filter()
# def range(min=5):
    # return range(min)

def loginsystem(request):
    if request.method == "POST":
        loginusername = request.POST.get('emaillog')
        loginpassword = request.POST.get('password')
        user = authenticate(request, username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            request.session['name'] = loginusername
            msg = "Successfully logged in!!"
            return redirect("shop:Shophome")
        else:
            msg = "Failed to log in!! please enter right password/ username!!"

        return render(request, 'shop/login.html', context={"msg": msg})

    return render(request, 'shop/login.html')


def signupsys(request):
    s_stat = "Register here!!"
    color = "dark"
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(username)
        s_stat = "Register here!"

        if password == password2 and len(password) >= 8:
            finalpassword = password
            user = User.objects.create_user(username, email,finalpassword)
            user.save()
            request.session['name'] = username
            Profile.objects.create(username=username, purchased_items = [0], user_email = email)
            
            s_stat = "Registration successful!!"
            color = "success"
        elif len(password) < 8:
            s_stat = "Password must be equal to or greater than 8 characters!!"
            color = "danger"
        else:
            s_stat = "Sorry! failed to register! check your passwords once again..."
            color = "danger"

    return render(request, 'shop/register.html', context={"s_stat": s_stat, "color":color })


def logout_view(request):

        logout(request)
        return redirect("shop:Shophome")

