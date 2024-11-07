from django import template
from cadmin.models import *
register = template.Library()
import json

# @register.filter()
# def applydiscount(pid):
#     data = Product.objects.get(id=pid)
#     price = data.price if data.price else 0  
#     discount = data.discount if data.discount else 0 
#     try:
#         final_price = int(price) * (100 - int(discount)) / 100
#     except ValueError:
#         final_price = 0
#     return final_price

@register.filter()
def applydiscount(pid):
    data = Product.objects.get(id=pid)
    try:
        price = float(data.price) if data.price else 0  
        discount = float(data.discount) if data.discount else 0 
        
        if discount > 0:  # Only calculate discount if it exists
            final_price = price * (100 - discount) / 100
            return {
                'original_price': price,
                'final_price': final_price,
                'has_discount': True
            }
        else:
            return {
                'original_price': price,
                'final_price': price,
                'has_discount': False
            }
    except (ValueError, TypeError):
        return {
            'original_price': 0,
            'final_price': 0,
            'has_discount': False
        }
    
@register.filter()
def productimage(pid):
    data = Product.objects.get(id=pid)
    return data.image.url

@register.filter()
def productname(pid):
    data = Product.objects.get(id=pid)
    return data.name

@register.filter()
def productprice(pid):
    data = Product.objects.get(id=pid)
    return data.price

# @register.simple_tag
# def producttotalprice(data, qty):
#     product = Product.objects.get(id=data)
#     price = float(product.price) * (100 - float(product.discount)) / 100
#     return int(qty) * price

@register.simple_tag
def producttotalprice(data, qty):
    try:
        product = Product.objects.get(id=data)
        
        # Handle empty or invalid price and discount
        price = float(product.price) if product.price else 0.0
        discount = float(product.discount) if product.discount else 0.0
        
        # Apply the discount
        final_price = price * (100 - discount) / 100
        
        # Ensure qty is valid
        quantity = int(qty) if qty else 0
        
        # Calculate total price
        total_price = quantity * final_price
        
        return total_price
    
    except (ValueError, TypeError, Product.DoesNotExist):
        # Return 0 if there's any issue
        return 0


@register.filter()
def get_product(productli):
    try:
        productli = productli.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        print(myli)
        pro_li = []
        for i, j in myli.items():
            pro_li.append(int(i))
        product = Product.objects.filter(id__in=pro_li)
        print(product)
        return product
    except:
        return None

@register.simple_tag
def get_qty(pro, bookid):
    try:
        book = Booking.objects.get(id=bookid)
        productli = book.product.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        return myli[str(pro)]
    except:
        return 0