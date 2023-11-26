from django.shortcuts import render, redirect
from django.views import View
from home.models import Product
from .cart import Cart
from .forms import CartAddForm


# Create your views here.
class CartView(View):
    def get(self, request):
        return render(request, 'orders/cart.html')


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart()
        product = Product.objects.get(id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product=product,quantity=form.cleaned_data['quantity'])
        return redirect('orders:cart')