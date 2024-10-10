from django.contrib import messages

from django.views.generic import View

from .models import Commodity, Favorite, Cart

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import  jf_Commodity, ExchangeHistory
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Commodity, User, Cart


# Create your views here.

def is_login(view_func):
    def inner(request, *args, **kwargs):
        if request.session.get("username"):
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'url': '/login', 'code': -1, 'msg': '登录后才能评论'})

    return inner


def Index(request):
    return render(request, 'items-robots/index.html')


def logout(request):
    request.session.flush()
    return render(request, 'items-robots/logout.html')


def discount(request):
    return render(request, 'items-robots/discount.html')


def face(request):
    return render(request, 'items-robots/face.html')


def identity(request):
    return render(request, 'items-robots/identity.html')


def exchange(request):
    return render(request, 'items-robots/exchange.html')


# def Commodity(request):
#     return render(request, 'items-robots/../templates/shopping.html')

def logined(request):
    user_id = request.session.get('user_id')
    user=User.objects.get(id=user_id)
    context={
        'user':user
    }
    return render(request, 'items-robots/logined.html',context=context)


class Login(View):
    def get(self, request):
        return render(request, 'items-robots/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not all([username, password]):
            return JsonResponse({'code': 0, "msg": "有必填项未填"})

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'code': 0, 'msg': '账号不存在'})

        request.session['username'] = user.username
        request.session['user_id'] = user.id
        request.session.set_expiry(60 * 60 * 24)
        return JsonResponse({'code': 1, 'msg': '登录成功', 'url': '/logined', "username": username, 'password': password})


class Reg(View):
    def get(self, request):
        return render(request, 'items-robots/register.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        tel = request.POST.get("tel")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        view_difficult = request.POST.get("view_difficult")
        Consumption_frequency = request.POST.get("Consumption_frequency")
        fen = request.POST.get("fen")
        try:
            u = User(username=username, password=password, tel=tel, gender=gender, age=age,
                     view_difficult=view_difficult, Consumption_frequency=0, fen=0)
            u.save()
            request.session['username'] = u.username
            # request.session['user_id']=u.id
            request.session.set_expiry(60 * 60 * 24)
            return JsonResponse(
                {'code': 1, 'msg': '注册成功', 'url': '/logined', "username": username, 'password': password})
        except  Exception as e:
            return JsonResponse({'code': 0, 'msg': f'数据保存失败:{e}'})


def switchuser(request):
    if "username" in request.session.keys():
        del request.session['username']

    return HttpResponseRedirect('/')


# class Commodity(ListView):
#     model = Commodity
#     templates_name = 'shopping.html'
#     context_object_name = 'post'
#
#     def get_queryset(self):
#         return super(Index,self).get_queryset()
#
#     def get_context_data(self,  **kwargs):
#         content={
#             ''
#         }
def Commodity_view(request):
    commodity_all = Commodity.objects.all()
    user_id = request.session.get('user_id')
    context = {
        'commodity': commodity_all
    }
    return render(request, 'shopping.html', context=context)
    # return render(request,'shopping.html')


def jf_Commodity_view(request):
    commodity_all = jf_Commodity.objects.all()
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    context = {
        'jf_commodity': commodity_all,
        'user': user
    }
    return render(request, 'items-robots/integration.html', context=context)


# 收藏夹


@require_POST
def favorite_product(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'not_logged_in', 'message': 'User not logged in.'})

    import json
    data = json.loads(request.body)
    product_id = data.get('product_id')

    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'Product ID is required.'})

    try:
        product = Commodity.objects.get(id=product_id)
    except Commodity.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found.'})

    user = User.objects.get(id=user_id)
    favorite, created = Favorite.objects.get_or_create(user=user, product=product)
    if not created:
        # 商品已经在收藏夹中，更新数量
        favorite.save()

    return JsonResponse({'status': 'success', 'message': 'Product favorited successfully.'})


def favorite_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponseRedirect('/login')

    user = User.objects.get(id=user_id)
    favorites = Favorite.objects.filter(user=user).select_related('product')
    context = {
        'favorites': favorites
    }
    return render(request, 'items-robots/favorite.html', context)


def remove_favorite(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponseRedirect('/login')

    user = User.objects.get(id=user_id)
    favorite = get_object_or_404(Favorite, user=user, product_id=product_id)
    favorite.delete()
    return redirect('favorite_list')


def exchange_product(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponseRedirect('/login')

    user = User.objects.get(id=user_id)
    product = get_object_or_404(jf_Commodity, id=product_id)

    if user.fen < product.price:
        messages.error(request, '积分不足，无法兑换该商品。')
        return redirect('jf_commodity_list')  # 假设这是积分商品列表的视图名称

    user.fen -= product.price
    user.save()

    # 保存兑换记录
    exchange_history = ExchangeHistory(user=user, product=product)
    exchange_history.save()

    messages.success(request, '商品兑换成功！')
    return redirect('jf_commodity_list')  # 假设这是积分商品列表的视图名称


def jf_commodity_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponseRedirect('/login')

    user = User.objects.get(id=user_id)
    jf_commodity = jf_Commodity.objects.all()

    context = {
        'user': user,
        'jf_commodity': jf_commodity,
    }
    return render(request, 'items-robots/integration.html', context)


# 购物车
@require_POST
def addcart(request):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'not_logged_in', 'message': 'User not logged in.'})

        import json
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'Product ID is required.'})

        try:
            product = Commodity.objects.get(id=product_id)
        except Commodity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'})

        user = User.objects.get(id=user_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            # 商品已经在购物车中，更新数量
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1  # 确保新创建的购物车项有默认数量
            cart_item.save()

        return JsonResponse({'status': 'success', 'message': 'Product added to cart successfully.'})
    except Exception as e:
        # 捕获所有异常，并返回错误信息
        return JsonResponse({'status': 'error', 'message': str(e)})

def cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponseRedirect('/login')

    user = User.objects.get(id=user_id)
    cart = Cart.objects.filter(user=user).select_related('product')
    context = {
        'cart': cart
    }
    return render(request, 'items-robots/shopping_cart.html', context)
