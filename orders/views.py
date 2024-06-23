from django.shortcuts import render,redirect
from .models import Order,OrderedItem
from products.models import Product
from customers.models import Customer
from django.contrib import messages

# Create your views here.

def show_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer_profile
        cart = Order.objects.filter(owner=customer, order_status=Order.CART_STAGE).first()
    else:
        cart = None
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product=Product.objects.get(pk=product_id)
        ordered_item=OrderedItem.objects.create(
            product=product,
            owner=cart_obj,
            
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()
    return redirect('cart')
def remove_item_from_cart(request,pk):
    item=OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect ('cart')


def checkout_cart(request):
    if request.POST:
        try:
            user=request.user
            customer=user.customer_profile
            total=float(request.POST.get('total'))
            
            order_obj,created=Order.objects.get_or_create(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.total_price=total
                order_obj.save()
                status_message="Your order is processed.Your items will be delivered in 3 days"
                messages.success(request,status_message)
            else:
                error_message="Unable to processed.No items in cart"
                messages.success(request,error_message)
        except Exception as e:
            error_message="Unable to processed.No items in cart"
            messages.success(request,error_message)
    return redirect('cart')
