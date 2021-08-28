from django.http import HttpResponse
from django.shortcuts import render
from itertools import islice
from . import forms
from . import models

from cart.forms import CartAddProductForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Value

import datetime
import re
# thư viện cho việc sử dụng email
from SportStore.settings import EMAIL_HOST_USER
from django.core.mail import message, send_mail

from django.core.mail import EmailMultiAlternatives

# Global var

subcategory_list = models.SubCategory.objects.all()
subcategory = 0
search_str = ''

# Create your views here.

def index(request):
    username = request.session.get('username', 0)
    tbgd = models.SubCategory.objects.filter(category=1)
    ddnb = models.SubCategory.objects.filter(category=2)
    product_list = models.Product.objects.order_by("-public_day")
    most_viewed_list = models.Product.objects.order_by("-viewed")[:4]
    newest = product_list[0]
    four_newest = product_list[:8]
    four_oldest = list(islice(reversed(product_list),0,8))

    return render(request, "store/index.html",
                  {'newest': newest,
                   'four_oldest': four_oldest,
                   'four_newest': four_newest,
                   'most_viewed_list': most_viewed_list,
                   'subcategories': subcategory_list,
                   'tbgd': tbgd,
                   'ddnb': ddnb,
                   'username': username,
                   })

def cart(request):
    username = request.session.get('username', 0)
    return render(request, 'store/cart.html',
                  {'subcategories': subcategory_list,
                   'username': username
                   })

def account(request):
    return render(request,"store/account.html")

def contact(request):
    now = datetime.datetime.now()
    fullname = request.session.get('fullname', 0)
    if request.method == 'POST':
        form_contact = forms.ContactForm(request.POST)
        if (form_contact.is_valid()):
            email_address = request.POST.get('email')
            subject = '<b><h2>Welcome to SportStore</h2></b>'
            message = 'Hope you are enjoying our service'
            recepient = str(email_address)

            html_content = '<h2 style="color:blue"><i>Kính chào '+ form_contact.cleaned_data['fullname']+',</i></h2>'\
                            + '<p>Chào mừng quý khách đến với <strong>SportStore</strong> website.</p>' \
                            + '<h4 style="color:red">'+ message +'</h4>'      
            
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            result = 'Our mail was sent to your mail box. Thank you'

            return render(request, 'store/contact.html',
                    {'subcategories': subcategory_list, 
                    'form_contact': form_contact,
                    'today': now,
                    'fullname': fullname,
                    'result': result,
                    }
                    )
        else:
            form_contact = forms.ContactForm()


    return render(request, 'store/contact.html',
                  {'subcategories': subcategory_list, 
                   'today': now,
                   'fullname': fullname,
                   }
                  )

    
def products_detail(request,pk):
    username = request.session.get('username', 0)
    product_select = models.Product.objects.get(pk=pk)
    # khi người dùng chọn xem 1 sản phẩm > tăng view của sản phẩm thêm 1
    models.Product.objects.filter(
        pk=product_select.pk).update(viewed=F('viewed') + 1)
    product_select.refresh_from_db()
    cart_product_form = CartAddProductForm()
    return render(request, "store/products_detail.html",
                  {'product': product_select,
                   'subcategories': subcategory_list,
                   'username': username,
                   'cart_product_form': cart_product_form,
                   })

def products(request,pk):
    username = request.session.get('username', 0)
    subcategory = pk
    product_list = []
    subcategory_name = ''
    if pk != 0:
        product_list = models.Product.objects.filter(
            subcategory=pk).order_by("-public_day")
        selected_sub = models.SubCategory.objects.get(pk=pk)
        subcategory_name = selected_sub.name
    else:
        product_list = models.Product.objects.order_by("-public_day")

    three_newest = product_list[:3]

    page = request.GET.get('page', 1)  # trang bat dau
    paginator = Paginator(product_list, 8)  # so product/trang

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "store/products.html",
                  {'three_newest': three_newest,
                   'subcategories': subcategory_list,
                   'products': products,
                   'pk': pk,
                   'subcategories': subcategory_list,
                   'subcategory_name': subcategory_name,
                   'username': username
                   })

def sign_in(request):
    # registered = False
    # if request.method == "POST":
    #     form_cus = forms.FormCustumer(data=request.POST)
    #     if (form_cus.is_valid() and (form_cus.cleaned_data['password'] == form_cus.cleaned_data['confirm'])):
    #         user = form_cus.save()
    #         user.save()
    #         registered = True

    #     if (form_cus.cleaned_data['password'] != form_cus.cleaned_data['confirm']):
    #         form_cus.add_error('confirm', 'Password và confirm password khác nhau!!!')
    #         print(form_cus.errors)
    # else:
    #     form_cus = forms.FormCustumer()

    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            registered = True

            # Gửi email 
            email_address = form_user.cleaned_data['email']        
            subject = 'Tài khoản của Quý khách tại SportStore đã được tạo.'
            message = 'Hãy trải nghiệm việc mua sắm online tại SportStore.<br/> Trân trọng.'
            recepient = str(email_address)

            html_content = '<h2 style="color:blue"><i>Kính chào '+ form_user.cleaned_data['username']+',</i></h2>'\
                        + '<p>Chào mừng quý khách đến với <strong>SportStore</strong> website.</p>' \
                        + '<h4 style="color:red">'+ message +'</h4>'      
        
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error(
                'confirm', 'Password và confirm password không giống nhau!')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    username = request.session.get('username', 0)
    return render(request, 'store/signin.html',
                  {'subcategories': subcategory_list,
                   'form_user': form_user,
                   'form_por': form_por,
                   'registered': registered,
                   'username': username}
                  )


def log_in(request):
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user = models.Customer.objects.filter(username=username, password=password)
    #     if user is not None:
    #         result = "Xin chào quý khách " + username
    #         request.session['username'] = username
    #         username = request.session.get('username', 0)
    #         return render(request, "store/login.html", {'login_result': result,
    #                                                       'username': username})
    #     else:
    #         login_result = "Username hoặc password không chính xác."
    #         return render(request, "store/login.html", {'login_result': login_result})
    # else:
    #     return render(request, "store/login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, "store/login.html", {'login_result': result,
                                                        'username': username,'subcategories': subcategory_list,
                                                        })
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username hoặc password không chính xác!"
            return render(request, "store/login.html", {'login_result': login_result, 'subcategories': subcategory_list,})
    else:
        return render(request, "store/login.html", {'subcategories': subcategory_list})


@login_required
def log_out(request):
    # try:
    #     del request.session['username']
    # except KeyError:
    #     pass
    # logout = "Quý khách đã logout. Quý khách có thể login trở lại"
    # return render(request, "store/login.html", {'logout': logout})
    logout(request)
    result = "Quý khách đã logout. Quý khách có thể login trở lại"
    return render(request, "store/login.html", {'logout_result': result, 'subcategories': subcategory_list,})
