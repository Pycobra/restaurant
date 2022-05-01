from django.conf import settings

from apps.product.models import Product
from apps.checkout.models import DeliveryOptions

from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        for i in self.cart.keys():
            self.cart[str(i)]['product'] = Product.objects.get(pk=i)
        for item in self.cart.values():
            total = int(item['product'].price) * int(item['quantity'])
            if item['product'].discount_price:
                total = int(item['product'].discount_price) * int(item['quantity'])
            item['total_price'] = total
            yield item

    """i.chats.product.category.slug
    {'chats': {'5': {'id': '5', 'quantity': 1, 'price': 1, 'total_price': 1, 'product':}}"""
    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def add(self, product_id, product, quantity, update_quantity=False):
        product_id = str(product_id)
        new=((int(product.discount_price)/int(product.price)) * 100)
        discount_percent = int(100 - new)
        discount_amt = (int(product.price) - int(product.discount_price))

        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            product_exist = True
        if product_id not in self.cart:
            self.cart[product_id] = {'id': product_id, 'quantity':quantity, 'total_price':0,
                                     'price':product.price, 'discount_price':product.discount_price, 'discount_percent':discount_percent, 'discount_amt':discount_amt}
            product_exist = False
        self.save()
        return product_exist

    def update(self, product_id, product, quantity=1, update_quantity=True):
        product_id = str(product_id)
        sub_total=0
        item_total_cost=0
        total=0
        delivery_price=0
        item_quantity=0
        if product_id in self.cart and update_quantity == True:
            self.cart[product_id]['quantity'] += int(quantity)
            self.cart[product_id]['total_price'] = self.cart[product_id]['price'] * self.cart[product_id]['quantity']
            if self.cart[product_id]['discount_price']:
                self.cart[product_id]['total_price'] = self.cart[product_id]['discount_price'] * self.cart[product_id]['quantity']
            item_total_cost = self.cart[product_id]['total_price']
            sub_total = self.get_subtotal_cost()
            delivery_price = self.get_delivery_price()
            total = sub_total + delivery_price
            item_quantity=self.cart[product_id]['quantity']
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        self.save()
        #return item_quantity, Decimals(item_total_cost), Decimals(sub_total), Decimals(total), Decimals(delivery_price)
        return item_quantity, item_total_cost, sub_total, total, delivery_price


    def subtract(self,product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)
        sub_total=0
        item_total_cost=0
        total=0
        delivery_price=0
        item_quantity=0
        if product_id not in self.cart:
            pass
        if update_quantity:
            self.cart[product_id]['quantity'] -= int(quantity)
            self.cart[product_id]['total_price'] = self.cart[product_id]['price'] * self.cart[product_id][
                'quantity']
            if self.cart[product_id]['discount_price']:
                self.cart[product_id]['total_price'] = self.cart[product_id]['discount_price'] * \
                                                       self.cart[product_id]['quantity']

            item_total_cost = self.cart[product_id]['total_price']
            sub_total = self.get_subtotal_cost()
            delivery_price = self.get_delivery_price()
            total = sub_total + delivery_price
            item_quantity = self.cart[product_id]['quantity']
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        self.save()
        #return item_quantity, Decimals(item_total_cost), Decimals(sub_total), Decimals(total), Decimals(delivery_price)
        return item_quantity, item_total_cost, sub_total, total, delivery_price

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            item_quantity = self.cart[product_id]['quantity']
            item_total_cost = self.cart[product_id]['total_price']
            delivery_price = self.get_delivery_price()
            del self.cart[product_id]
            self.save()
            sub_total = self.get_subtotal_cost()
            total = sub_total + delivery_price
            # return item_quantity, Decimals(item_total_cost), Decimals(sub_total), Decimals(total), Decimals(delivery_price)
            return item_quantity, item_total_cost, sub_total, total, delivery_price

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_subtotal_cost(self):
        total=sum(item['quantity'] * item['price'] for item in self.cart.values())
        discount = (item['discount_price'] for item in self.cart.values())
        if discount:
            total = sum(item['quantity'] * item['discount_price'] for item in self.cart.values())

        return total

    def get_total_cost(self):
        newprice = 0
        subtotal = sum(item['price'] * item["quantity"] for item in self.cart.values())
        discount = (item['discount_price'] for item in self.cart.values())
        if discount:
            subtotal = sum(item['quantity'] * item['discount_price'] for item in self.cart.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + newprice
        # return Decimal(total)
        return total

    def get_delivery_price(self):
        newprice = 0
        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
        return newprice


    def cart_update_delivery(self, deliveryprice=0):
        subtotal = sum(item["price"] * item["quantity"] for item in self.cart.values())
        discount = (item['discount_price'] for item in self.cart.values())
        if discount:
            subtotal = sum(item['quantity'] * item['discount_price'] for item in self.cart.values())

        total = subtotal + deliveryprice
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session['address ']
        del self.session['purchase']
        self.save()