from django import template
# from ..models import Person, Product

register = template.Library()

# @register.filter
# def get_customer(value, attr):
#     return getattr(Person.objects.get(id=int(value)), attr)

# @register.filter
# def get_product(value, attr):
#     return getattr(Product.objects.get(id=int(value)), attr)

# @register.filter
# def total_price(value, attr):
#     return attr * getattr(Product.objects.get(id=int(value)), 'price')

# register.tag('get_customer',get_customer)
# register.tag('get_product',get_product)
# register.tag('total_price',total_price)