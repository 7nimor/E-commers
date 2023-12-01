from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from home.models import Product
from .cart import Cart
from .forms import CartAddForm
from .models import Order, OrderItem


# Create your views here.
class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/detail.html', {'order': order})


class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        order=Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],price=item['price'])
        cart.clean()
        return redirect('orders:order_detail',order.id)
