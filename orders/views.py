from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
#from .tasks import order_created
from store import models

# thư viện cho việc sử dụng email
from SportStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives


subcategory_list = models.SubCategory.objects.all()


def order_create(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    if username:
        user = models.User.objects.get(username=username)
        
        order = Order()
        order.username = user.username
        order.first_name = user.first_name
        order.last_name = user.last_name
        order.email = user.email
        
        if not user.is_staff:
            user_profile = models.UserProfileInfo.objects.get(user=user)
            order.phone = user_profile.phone
            order.address = user_profile.address
    else:
        order = Order()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, order)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # Gửi email
            email_address = form.cleaned_data['email']
            subject = 'Xác nhận đơn hàng ' + str(order.id)
            message = 'Cảm ơn quý khách <b>' + order.last_name + \
                ' ' + order.first_name + '</b> đã đặt hàng tại Tiki,'
            recepient = str(email_address)

            html_content = '''
            <p style="margin:4px 0;font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#444;line-height:18px;font-weight:normal;">SportStore rất vui thông báo đơn hàng ''' + \
                str(order.id) + \
                ''' của quý khách đã được tiếp nhận và đang trong quá trình xử lý. </p>									
			<h3 style="font-size:13px;font-weight:bold;color:#02acea;text-transform:uppercase;margin:20px 0 0 0;border-bottom:1px solid #ddd;">Thông tin đơn hàng:</h3>''' + \
                '''<h5>Họ và tên: ''' + \
                order.last_name + \
                ''' ''' + \
                order.first_name + \
                '''</h5> ''' + \
                '<h5>Phone: ' + \
                str(order.phone) + \
                '''</h5><h5>Địa chỉ giao hàng: ''' + \
                order.address + \
                '''</h5> ''' + \
                '''<h2 style="text-align:left;margin:10px 0;border-bottom:1px solid #ddd;padding-bottom:5px;font-size:13px;color:#02acea;">CHI TIẾT ĐƠN HÀNG</h2>''' + \
                '''<table border="0" cellpadding="0" cellspacing="0" style="background:#f5f5f5;" width="100%">''' + \
                ''' <thead>
											<tr>
												<th align="left" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Sản phẩm</th>
												<th align="left" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Đơn giá</th>
												<th align="left" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Số lượng</th>
												<th align="right" bgcolor="#02acea" style="padding:6px 9px;color:#fff;font-family:Arial, Helvetica, sans-serif;font-size:12px;line-height:14px;">Tổng tạm</th>
											</tr>
										</thead>
                                        <tbody style="font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#444;line-height:18px;">
            '''
            for item in cart:
                html_content += '''
                <tr>
					<td align="left" style="padding:3px 9px;" valign="top"><span class="yiv1530170030name">''' + \
                    str(item['product']) + \
                    '''</td>''' + \
                    '''<td align="left" style="padding:3px 9px;" valign="top"><span>''' + \
                    str("{:0,.0f}".format(item['price'])) + \
                    '''</span></td>''' + \
                    ''' <td align="left" style="padding:3px 9px;" valign="top">''' + \
                    str(item['quantity']) + \
                    '''</td>''' + \
                    '''<td align="right" style="padding:3px 9px;" valign="top"><span>''' + \
                    str("{:0,.0f}".format(item['total_price'])) + \
                    '''</span></td></tr>'''
            html_content += '''<tr><td colspan="4" style="text-align:right">Tổng đơn hàng:''' + \
                str("{:0,.0f}".format(cart.get_total_price())) + \
                '''đ</td></tr>'''
            html_content += '''</table>

            <p style="margin:0;font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#444;line-height:18px;font-weight:normal;">Trường hợp quý khách có những băn khoăn về đơn hàng, có thể liên hệ với chúng tôi theo số <b>(028) 38 351 056</b></p>'''

            msg = EmailMultiAlternatives(
                subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # clear the cart
            cart.clear()

            return render(request,
                          'orders/order/created.html',
                          {'order': order, 'subcategories': subcategory_list, 'username': username})
    else:
        form = OrderCreateForm(instance=order)
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form, 'subcategories': subcategory_list, 'username': username})
