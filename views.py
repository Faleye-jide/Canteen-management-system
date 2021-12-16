from django.shortcuts import render, redirect
from django.views import View
from .form import ContactForm, SignUpForm
from .models import MenuItem, Category, Contact, Order as OrderModel
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.urls import reverse


class index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Customer/index.html')

class contact(View):
    def get(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'Customer/success.html')
        form = ContactForm()
        context = {
            "contactForm": form
        }

        return render(request, 'Customer/contact.html', context)

def success(request):
    return render(request,'Customer/success.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Customer/about.html')

def register(request):
    # def get(self, request, *args, **kwargs):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password = password)
            auth_login(request, user)
            messages.success(request, "Your registration is successful, Account was created for " + user.username)
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid Information")
    form = SignUpForm

    context = {
        "signUpForm" : form
    }
    return render(request, 'Customer/register.html', context)

def login(request):
    # def get(self, request, *args, **kwargs):
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # username = request.POST.get('username')
            # password = request.POST.get('password')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user:
                auth_login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    # elif request.method == 'GET':
    form = AuthenticationForm()

    context = {
        "loginform": form
    }
    return render(request, 'Customer/login.html', context)

def logout(request):
    auth_logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('login')
    # return HttpResponseRedirect(reverse('login'))

class menuView(View):
    # @login_required(login_url='login')
    def get(self, request, *args, **kwargs):
        meal = MenuItem.objects.all()
        search_item = ""
        if 'search' in request.GET:
            search_item = request.GET.get['search']
            meal = MenuItem.objects.filter(text_icontains=search_item)


        context = {
            "menu":meal,
            "search_item":search_item
        }
        return render(request, 'Customer/menu.html', context)


class MY_ORDERS(View):
    # @login_required(login_url='login')
    def get(self, request, *args, **kwargs):
        user = request.user
        order = OrderModel.objects.filter(user=user)
        print(f"user {order}")
        total_pay = 0
        for ord in order:
            total_pay += ord.price

        context = {
            "order": order,
            "total_pay":total_pay
        }
        # send confirmation email to the user
        # message = ("Thank you for your order! your food is being processed soon!\n"
        #         f'Your total pay is {total_pay}\n'
        #         'Thank you again for your order!')
        #
        # send_mail(
        #     'Thank You for Your Order!',
        #     message,
        #     'faleyejide@gmail.com',
        #     [email],
        #     fail_silently=False,
        # )
        return render(request, "Customer/orderConfirmation.html", context)

class searchMenu(View):
    def get(self, request,*args, **kwargs):
        search = request.GET.get("q")

        meals = MenuItem.objects.filter(
            Q(name__icontains=search)|
            Q(price__icontains=search)|
            Q(description__icontains=search)
            )

        context = {
            'meals': meals
        }
        return render(request, 'Customer/search_result.html', context)

class Order(View):
    # @login_required(login_url='login')
    def get(self, request, *args, **kwargs):
    # get every item from the category

        appetizer = MenuItem.objects.filter(category__name__contains='Starter')
        breakfast = MenuItem.objects.filter(category__name__contains='Breakfast')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')
        dessert = MenuItem.objects.filter(category__name__contains='Dessert')
        lunch = MenuItem.objects.filter(category__name__contains='Lunch')
        # appetizers = MenuItem.objects.filter(category_name_contains='')
        # pass the context

        context ={
            "appetizers": appetizer,
            "lunch": lunch,
            "drinks": drinks,
            "breakfast": breakfast,
            "Desserts": dessert
        }
        # render the template
        return render(request, 'Customer/order.html', context)

    def post(self, request, *args, **kwargs):
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        # street = request.POST.get('street')
        # city = request.POST.get('city')
        # postcode = request.POST.get('postcode')
        print(f"{request.user.userOrder}")

        order_items = {
            "items":[]
        }
        items = request.POST.getlist('items[]')
        print(f"items {items}")

        for item in items:
            print(f"item id {item}")
            if item:
                item = int(item)
                menu_item = MenuItem.objects.get(pk=item)
                check_value = OrderModel.objects.filter(user=request.user, menu_item=menu_item)
                if len(check_value) < 1:
                    orders = OrderModel.objects.create(
                        price = menu_item.price,
                        user = request.user,
                        menu_item = menu_item
                    )
                    print(f"order created {orders}")


        # context ={
        #     'orders': orders,
        #     'total_pay':total_pay
        # }
        # return render(request, 'Customer/orderConfirmation.html', )

            # order_items['items'].append(item_details)
            # print(order_items)
        #
        #     price = 0
        #     item_ids = []
        #
        # for item in order_items['items']:
        #     price += item['price']
        #     item_ids.append(item['id'])
        #
        # order = OrderModel.objects.create(
        #     price =price,
        #     name=name,
        #     email=email,
        #     street=street,
        #     city=city,
        #     postCode=postcode
        # )
        # order.items.add(*item_ids)

    #

        # context = {
        #     'items': order_items['items'],
        #     'price': price
        # }

        return render(request, 'Customer/orderConfirmation.html')
        # return redirect('order-confirmation', pk=order.pk)